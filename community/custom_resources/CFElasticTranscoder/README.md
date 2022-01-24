# ElasticTranscoder

[CloudFormation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/Welcome.html) does not seem to provide a way to create [ElasticTranscoder](https://docs.aws.amazon.com/elastictranscoder/latest/developerguide/introduction.html) Pipelines and Presets. This example provide two [Custom Resource](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/template-custom-resources.html) that allow you to create Pipelines and Presets from within your Cloudformation template.

## Create the Custom Resources

In order to be able to create ElasticTranscoder Pipelines and Presets from your CloudFormation template, you will first need to use SAM to build and deploy these Custom Resources:

```bash
cd resources/ElasticTranscoderPipeline
sam build
sam deploy
cd ../../resources/ElasticTranscoderPreset
sam build
sam deploy
```

## Using the Custom Resources

You can then reference the newly cerated Resources in your CloudFormation template.
There is a example that show case the use of these Custom Resources. It creates an S3 Bucket <InputBucket> where the user can upload an video and, after conversion, can download the resulting video in the S3 Bucket <OutputBucket>. An IAM user is created with access limited to these 2 buckets.

In order to create the example stack execute:

```bash
sam build --template ElasticTranscoder.yaml
sam deploy --capabilities "CAPABILITY_IAM CAPABILITY_NAMED_IAM"
```

Once ready you will need to configure your AWS CLI 

```bash
aws configure --profile elastictranscoder
AWS Access Key ID [None]: <AccessKeyId>
AWS Secret Access Key [None]: <SecretAccessKey>
Default region name [None]: <Region>
Default output format [None]: 
```

You can finally upload your video for conversion 

```bash
aws --profile elastictranscoder s3 cp /path/to/video.mp4 s3://<InputBucket>
aws --profile elastictranscoder s3 cp s3://<OutputBucket> /path/to/converted_video.mp4
```

*BEWARE*: The example stack uses the [SamPolicyTemplateTranslator](https://github.com/awslabs/aws-cloudformation-templates) CloudFormation Macros. You will need to have created them in your accoutn before hand

## Cleaning up

```bash
aws s3 rm --recursive s3://<InputBucket>
aws s3 rm --recursive s3://<OutputBucket>
aws cloudformation delete-stack --stack-name ElasticTranscoder
```
