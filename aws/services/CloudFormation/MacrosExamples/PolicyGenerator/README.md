# How to install and use the PolicyGenerator macro in your AWS account

The `PolicyGenerator` macro Provides shorthand policy for KMS Key and S3 Bucket.

## Deploying

1. You will need an S3 bucket to store the CloudFormation artifacts:
    * If you don't have one already, create one with `aws s3 mb s3://<bucket name>`

2. Package the CloudFormation template. The provided template uses [the AWS Serverless Application Model](https://aws.amazon.com/about-aws/whats-new/2016/11/introducing-the-aws-serverless-application-model/) so must be transformed before you can deploy it.

    ```shell
    sam build
    ```

3. Deploy the packaged CloudFormation template to a CloudFormation stack:

    ```shell
    sam deploy --stack-name PolicyGenerator --capabilities CAPABILITY_IAM
    ```

4. To test out the macro's capabilities, try launching the provided example template:

    ```shell
    aws cloudformation deploy \
        --stack-name PolicyGenerator-example \
        --template-file template-example.yaml \
        --capabilities CAPABILITY_IAM
    ```

## Usage

To make use of the macro, add `Transform: PolicyGenerator` to the top level of your CloudFormation template.

Here is a trivial example template:

```yaml
AWSTemplateFormatVersion: '2010-09-09'
Transform: 
  - PolicyGenerator
Resources:
  Key:
    Type: AWS::KMS::Key
    Properties:
      Description: A key with a sane default policy
      KeyPolicy:
        - DefaultKeyPolicy:
            Administrator: Alice
            User: Bob
```

## Features

### Supported Object

So far only `AWS::KMS::Key`, `AWS::S3::BucketPolicy`, `AWS::SNS::TopicPolicy`, `AWS::SQS::QueuePolicy`.

## Author

[Julien Masnada](https://www.linkedin.com/in/julienmasnada)  

