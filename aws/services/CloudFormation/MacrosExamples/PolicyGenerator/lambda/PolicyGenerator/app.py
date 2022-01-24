from os.path import join, dirname, abspath
from samtranslator import policy_templates_data
from samtranslator.policy_template_processor.processor import PolicyTemplatesProcessor
from samtranslator.policy_template_processor.exceptions import InsufficientParameterValues, InvalidParameterValues
import logging
import uuid
import json

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Reference: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-policy.html
# Use the policy already defined in SAM
POLICY_TEMPLATES_FILE = join(dirname(abspath(__file__)), "policy_templates.json")
policy_templates = PolicyTemplatesProcessor._read_json(POLICY_TEMPLATES_FILE)
processor = PolicyTemplatesProcessor(policy_templates)

def generate_policy(policy: dict):
    """This method will convert a Policy Name into a KMS Key policy."""
    policy_name = next(iter(policy))
    policy_parameters = policy[policy_name]
    try:
        policy_document = processor.convert(policy_name, policy_parameters)
        policy_id = str(uuid.uuid4())
        policy_document['Id'] = f"{policy_name}-{policy_id}"
        return policy_document
    except Exception:
        raise ValueError(f"Invalid Parameter values for policy '{policy_name}'")


def handle_template(request_id, template):
    """Loop through the template and generate the given policy."""    
    for name, resource in template.get("Resources", {}).items():
        resource_type = resource["Type"]
        if resource_type == "AWS::KMS::Key":
            policy_key = "KeyPolicy"
            policy_version = "2012-10-17"
        elif resource_type == "AWS::S3::BucketPolicy":
            policy_key = "PolicyDocument"
            policy_version = "2012-10-17"
        elif resource_type == "AWS::SNS::TopicPolicy":
            policy_key = "PolicyDocument"
            policy_version = "2008-10-17"
        elif resource_type == "AWS::SQS::QueuePolicy":
            policy_key = "PolicyDocument"
            policy_version = "2012-10-17"
        else:
            continue
        properties = resource['Properties']
        if 'Version' in properties.get(policy_key, {}):
            # This is a normal policy document
            continue
        properties[policy_key] = generate_policy(properties[policy_key])
        properties[policy_key]['Version'] = policy_version
    return template


def lambda_handler(event, context):
    """Generate the template for the Policy."""    
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
    logger.debug (json.dumps(response))
    return response
