import copy
import json
from jsonpath_ng import jsonpath, parse

def process_node(node, new_template):
    if isinstance(node, dict) and node:
        for key in node:
            print(f"Processing {key}")
            if isinstance(node[key], dict) and node[key]:
                if 'BlockCopier' in node[key]:
                    blockCopierConfig = node[key].pop(
                        'BlockCopier')
                    if "Path" in blockCopierConfig:
                        print(
                            f"Found BlockCopier section in '{key}'")
                        copySourceBlockPathValue = blockCopierConfig["Path"]
                        json_path = parse(copySourceBlockPathValue)
                        match = json_path.find(new_template)
                        if (match):
                            copiedBlock = match[0].value
                            if "Replacements" in blockCopierConfig:
                                copiedBlockString = json.dumps(copiedBlock)
                                print(f"Processing replacements")
                                for replacementItem in blockCopierConfig["Replacements"]:
                                    original = replacementItem["Original"]
                                    replacement = replacementItem["Replacement"]
                                    print(f"Replacing '{original}' with '{replacement}'")
                                    copiedBlockString = copiedBlockString.replace(original,replacement)
                                copiedBlock = json.loads(copiedBlockString)
                            if isinstance(copiedBlock, dict) and copiedBlock:
                                node[key].update(copiedBlock)
                            elif isinstance(copiedBlock, list) and copiedBlock:
                                node[key] = copiedBlock
                            else:
                                raise TypeError(f"copiedBlock is an invalid type '{type(copiedBlock)}'")
                        else:
                            raise ValueError(
                                f"Nothing found in the template at the specified path ""{copySourceBlockPathValue}""")
                    else:
                        raise ValueError("Path parameter is missing from BlockCopier section")                    
                process_node(node[key], new_template)
            else:
                print("Null value")
    elif isinstance(node, list) and node:
        for item in node:
            process_node(item, new_template)
    return node

def process_template(template):
    new_template = copy.deepcopy(template)
    status = 'success'
    new_template['Resources'] = process_node(
        template['Resources'], new_template)
    return status, new_template


def handler(event, context):
    result = process_template(event['fragment'])
    return {
        'requestId': event['requestId'],
        'status': result[0],
        'fragment': result[1]
    }
