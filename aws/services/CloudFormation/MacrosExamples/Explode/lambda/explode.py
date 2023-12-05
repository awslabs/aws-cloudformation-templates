"""
CloudFormation template transform macro: Explode
"""

import re
import sys
import logging
import json

EXPLODE_RE = re.compile(r'(?i)!Explode (?P<explode_key>\w+)')
logger = logging.getLogger(__name__)

def walk_resource(resource, map_data):
    """Recursively process a resource."""
    if isinstance(resource, dict):
        new_resource = {}
        for key, value in resource.items():
            if isinstance(value, (dict, list)):
                new_resource[key] = walk_resource(value, map_data)
            elif isinstance(value, str):
                new_resource[key] = replace_explode_in_string(value, map_data)
            else:
                new_resource[key] = value
    elif isinstance(resource, list):
        new_resource = []
        for value in resource:
            if isinstance(value, (dict, list)):
                new_resource.append(walk_resource(value, map_data))
            elif isinstance(value, str):
                new_resource.append(replace_explode_in_string(value, map_data))
            else:
                new_resource.append(value)

    else:
        # if the resource is of type string
        new_resource = replace_explode_in_string(resource, map_data)
    return new_resource


def replace_explode_in_string(value, map_data):
    """Recursively process and replace Explode instances in a string."""
    match = EXPLODE_RE.search(value)
    while match:
        explode_key = match.group('explode_key')
        try:
            replace_value = map_data[explode_key]
        except KeyError:
            raise Exception ("Missing item {} in mapping while processing: {}\nMap Data:\n{}".format(
                explode_key,
                value,
                json.dumps(map_data, indent=4)))
        if isinstance(replace_value, int):
            value = replace_value
            # No further explosion is possible on an int
            match = None
        else:
            value = value.replace(match.group(0), replace_value)
            match = EXPLODE_RE.search(value)
    return value


def handle_section_transform(section, mappings):
    """Go through template and explode objects in the section."""
    new_section = {}
    for resource_name, resource in section.items():
        try:
            explode_map = resource['ExplodeMap']
            del resource['ExplodeMap']
        except KeyError:
            # This resource does not have an ExplodeMap, so copy it verbatim
            # and move on
            new_section[resource_name] = resource
            continue
        try:
            explode_map_data = mappings[explode_map]
        except KeyError:
            # This resource refers to a mapping entry which doesn't exist, so
            # fail
            raise Exception('Unable to find mapping for exploding object {}'.format(resource_name))
        resource_instances = explode_map_data.keys()
        for resource_instance in resource_instances:
            new_resource = walk_resource(resource, explode_map_data[resource_instance])
            if 'ResourceName' in explode_map_data[resource_instance]:
                new_resource_name = explode_map_data[resource_instance]['ResourceName']
            else:
                new_resource_name = resource_name + resource_instance
            new_section[new_resource_name] = new_resource
    return new_section


def handle_transform(fragment):
    """Go through template and explode objects in the fragment."""
    mappings = fragment['Mappings']
    if 'Conditions' in fragment:
        fragment['Conditions'] = handle_section_transform(fragment['Conditions'], mappings)
    fragment['Resources'] = handle_section_transform(fragment['Resources'], mappings)
    if 'Outputs' in fragment:
        fragment['Outputs'] = handle_section_transform(fragment['Outputs'], mappings)
    return fragment



def handler(event, _context):
    """Handle invocation in Lambda (when CloudFormation processes the Macro)"""
    fragment = event["fragment"]
    status = "success"

    try:
        fragment = handle_transform(fragment)
    except Exception as e:
        logger.error(e.__str__())
        status = "failure"

    return {
        "requestId": event["requestId"],
        "status": status,
        "fragment": fragment,
    }


if __name__ == "__main__":
    """
    If run from the command line, parse the file specified and output it
    This is quite naive; CF YAML tags like !GetAtt will break it (as will
    !Explode, but you can hide that in a string). Probably best to use JSON.
    Relatedly, always outputs JSON.
    """
    if len(sys.argv) == 2:
        filename = sys.argv[1]
        if filename.endswith(".yml") or filename.endswith(".yaml"):
            try:
                import yaml
            except ImportError:
                print("Please install PyYAML to test yaml templates")
                sys.exit(1)
            with open(filename, 'r') as file_handle:
                loaded_fragment = yaml.safe_load(file_handle)
        elif filename.endswith(".json"):
            with open(sys.argv[1], 'r') as file_handle:
                loaded_fragment = json.load(file_handle)
        else:
            print("Test file needs to end .yaml, .yml or .json")
            sys.exit(1)
        new_fragment = handle_transform(loaded_fragment)
        print(json.dumps(new_fragment,indent=4))