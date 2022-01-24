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
def create_preset(event, context):
    """Create a preset.
    """
    logger.info(json.dumps(event, indent=2))
    parameters = event['ResourceProperties']
    parameters.pop('ServiceToken', None)
    video = parameters.pop('Video', None)
    if video and isinstance(video, str):
        parameters['Video'] = json.loads(video)
    audio = parameters.pop('Audio', None)
    if audio and isinstance(audio, str):
        parameters['Audio'] = json.loads(audio)
    thumbnails = parameters.pop('Thumbnails', None)
    if thumbnails and isinstance(thumbnails, str):
        parameters['Thumbnails'] = json.loads(thumbnails)
    response = elastictranscoder.create_preset(**parameters)
    physical_id = response['Preset']['Id']
    helper.Data.update({"Arn": response['Preset']['Arn']})
    return physical_id

@helper.update
def update_preset(event, context):
    """Update the preset. The API does not allow updating a Preset
    """
    logger.error("Update of Preset is not supported by the underlying API. Creating a new resource")
    return create_preset(event, context)

@helper.delete
def delete_preset(event, context):
    """Delete the preset.
    """
    try:
        physical_id = event['PhysicalResourceId']
        elastictranscoder.delete_preset(Id=physical_id)
    except Exception as e:
        logger.error(str(e))

def lambda_handler(event, context):
    """Lambda function to create CustomResource of type ElasticTranscoderPreset

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
