import logging
import uuid
import json
from samtranslator import policy_templates_data
from samtranslator.policy_template_processor.processor import PolicyTemplatesProcessor
from samtranslator.policy_template_processor.exceptions import InsufficientParameterValues, InvalidParameterValues

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# Reference: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-policy.html
# Use the policy already defined in SAM
policy_templates = PolicyTemplatesProcessor.get_default_policy_templates_json()
processor = PolicyTemplatesProcessor(policy_templates)

def translate_policy(policy: dict):
    """This method will convert a SAM Policy template into an IAM policy

    Args:
        policy (dict): The policy to be expanded.
            If the attribute `PolicyName` is present then we consider that we are
            dealing with a normal policy

    Returns:
        policy: A policy document
    """
    if 'PolicyName' in policy:
        # This is a normal policy that should not be expanded
        return policy
    template_name = next(iter(policy))
    template_parameters = policy[template_name]
    try:
        # 'convert' will return a list of policy statements
        policy_document = processor.convert(template_name, template_parameters)
    except InsufficientParameterValues as e:
        # Exception's message will give lot of specific details
        raise ValueError(str(e))
    except InvalidParameterValues:
        raise ValueError("Must specify valid parameter values for policy template '{}'".format(template_name))
    return {
        "PolicyName": template_name + '-' + str(uuid.uuid4()),
        "PolicyDocument": policy_document
    }

def handle_template(request_id, template):
    for name, resource in template.get("Resources", {}).items():
        if resource["Type"] == "AWS::IAM::Role":
            props = resource["Properties"]
            if 'Policies' not in props:
                continue
            props["Policies"] = list(map(lambda p: translate_policy(p), props["Policies"]))
    return template

def lambda_handler(event, context):
    request_id = event["requestId"]
    fragment = event["fragment"]
    try:
        response = {
            "requestId": request_id,
            "status": "success",
            "fragment": handle_template(request_id, fragment),
        }
    except Exception as e:
        logger.error(e, exc_info=True)
        response = {
            "requestId": request_id,
            "status": "failure",
            "fragment": fragment,
            "errorMessage": str(e)
        }
    return response
