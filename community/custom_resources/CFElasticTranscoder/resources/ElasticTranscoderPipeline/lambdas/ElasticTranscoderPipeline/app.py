from crhelper import CfnResource
import boto3
import json
import logging


logger = logging.getLogger()
logger.setLevel(logging.INFO)

try:
    elastictranscoder = boto3.client('elastictranscoder')
except Exception as e:
    helper.init_failure(e)


# Look at documentation in https://github.com/aws-cloudformation/custom-resource-helper
helper = CfnResource()

@helper.create
def create_pipeline(event, context):
    """Create a pipeline.
    """
    parameters = event['ResourceProperties']
    parameters.pop('ServiceToken', None)
    response = elastictranscoder.create_pipeline(**parameters)
    physical_id = response['Pipeline']['Id']
    helper.Data.update({"Arn": response['Pipeline']['Arn']})
    return physical_id

@helper.update
def update_pipeline(event, context):
    """Update the pipeline.
    """
    physical_id = event['PhysicalResourceId']
    new_parameters = event['ResourceProperties']
    new_parameters.pop('ServiceToken', None)
    new_parameters.pop('OutputBucket', None)
    response = elastictranscoder.update_pipeline(
        Id=physical_id, 
        **new_parameters)
    physical_id = response['Pipeline']['Id']
    helper.Data.update({"Arn": response['Pipeline']['Arn']})
    return physical_id

@helper.delete
def delete_pipeline(event, context):
    """Delete the pipeline.
    """
    try:
        physical_id = event['PhysicalResourceId']
        elastictranscoder.delete_pipeline(Id=physical_id)
    except Exception as e:
        logger.error(str(e))

def lambda_handler(event, context):
    """Lambda function to create CustomResource of type ElasticTranscoderPipeline

    Parameters
    ----------
    event: dict, required
        Custom Resource request: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/crpg-ref-requests.html

    context: object, required
        Lambda Context runtime methods and attributes

        Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

    Returns
    ------
    CustomResourceResponse: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/crpg-ref-responses.html
    """
    helper(event, context)
