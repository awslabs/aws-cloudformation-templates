from urllib.parse import unquote_plus
import boto3
import json
import logging
import os

PIPELINE_NAME = os.environ['PIPELINE_NAME']
PIPELINE_ID = None
PRESET_ID = os.environ['PRESET_ID']

logger = logging.getLogger()
logger.setLevel(logging.INFO)

try:
    # I use the Pipeline name, because using the Pipeline Id
    # in the CloudFormation template generate a Circular 
    # dependency
    elastictranscoder = boto3.client('elastictranscoder')
    for pipeline in elastictranscoder.list_pipelines()['Pipelines']:
        if pipeline['Name'] == PIPELINE_NAME:
            PIPELINE_ID = pipeline['Id']
except Exception as e:
    logger.error(str(e))


def lambda_handler(event, context):
    """Trigger an ElasticTranscoder Job on newly uploaded S3 Files.
    """
    if not PIPELINE_ID: 
        raise ValueError(f"Invalid pipeline Name {PIPELINE_NAME}")

    for record in event['Records']:
        s3_bucket = unquote_plus(record['s3']['bucket']['name'])
        s3_key = unquote_plus(record['s3']['object']['key'])
        logger.debug(f"Creating Transcoding Job for s3://{s3_bucket}/{s3_key}")
        elastictranscoder.create_job(
            PipelineId=PIPELINE_ID,
            Inputs=[{
                "Key": s3_key,
                "FrameRate": "auto",
                "Resolution": "auto",
                "AspectRatio": "auto",
                "Interlaced": "auto",
                "Container": "mp4"
            }],
            Outputs=[{
                "Key": f"{PIPELINE_NAME}/{s3_key}",
                "Rotate": "0",
                "PresetId": PRESET_ID
            }]
        )
