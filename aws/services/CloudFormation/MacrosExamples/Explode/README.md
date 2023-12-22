# Explode CloudFormation Macro

The `Explode` macro provides a template-wide `Explode` property for CloudFormation resources, conditions and outputs. Similar to the Count macro, it will create multiple copies of a template Resource, but looks up values to inject into each copy in a Mapping, and this capability is expanded to Condition and Output statements in the template.

## How to install and use the Explode macro in your AWS account

### Deploying

1. You will need an S3 bucket to store the CloudFormation artifacts. If you don't have one already, create one with `aws s3 mb s3://<bucket name>`

2. Package the Macro CloudFormation template. The provided template uses [the AWS Serverless Application Model](https://aws.amazon.com/about-aws/whats-new/2016/11/introducing-the-aws-serverless-application-model/) so must be transformed before you can deploy it.

```shell
aws cloudformation package \
    --template-file macro.yml \
    --s3-bucket <your bucket name here> \
    --output-template-file packaged.yaml
```

3. Deploy the packaged CloudFormation template to a CloudFormation stack:

```shell
aws cloudformation deploy \
    --stack-name Explode-macro \
    --template-file packaged.yaml \
    --capabilities CAPABILITY_IAM
```

4. To test out the macro's capabilities, try launching the provided example template:

```shell
aws cloudformation deploy \
    --stack-name Explode-test \
    --template-file test.yaml \
    --capabilities CAPABILITY_IAM
```

### Usage

To make use of the macro, add `Transform: Explode` to the top level of your CloudFormation template.

Add a mapping (to the `Mappings` section of your template) which defines the instances of each template statement you want to explode by instantiating multiple times. Each entry in the mapping will be used for another copy of the resource/condition/output, and the values inside it will be copied into that instance. The entry name will be appended to the statement's name, unless a value `ResourceName` is given, which if present will be used as the complete instance name.  Note `ResourceName` is only useful if exploding a single statement as otherwise it creates naming conflicts.

For each statement you want to explode, add an `ExplodeMap` value at the top level pointing at the entry from your Mappings which should be used. You can use the same mapping against multiple resource entries.

Inside the resource properties, you can use `!Explode KEY` to pull the value of `KEY` out of your mapping.

An example is probably in order:

```yaml
AWSTemplateFormatVersion: "2010-09-09"
Transform: Explode
Mappings:
  BucketMap:
    Monthly:
      ResourceName: MyThirtyDayBucket
      Retention: 30
    Yearly:
      Retention: 365

Resources:
  Bucket:
    ExplodeMap: BucketMap
    Type: AWS::S3::Bucket
    Properties:
      LifecycleConfiguration:
        Rules:
          -
            ExpirationInDays: "!Explode Retention"
            Status: Enabled
```

This will result in two Bucket resources; one named `MyThirtyDayBucket` with a
lifecycle rule for 30 day retention, and another named `BucketYearly` with 365
day retention.

### Important - Naming resources

You cannot use Explode on resources that use a hardcoded name (`Name:`
property). Duplicate names will cause a CloudFormation runtime failure.
If you wish to specify a name then you must use `!Explode` with a mapped value
to make each resource's name unique.

For example:

```yaml
AWSTemplateFormatVersion: "2010-09-09"
Mappings:
  BucketMap:
    Example:
      Name: MyExampleBucket
Resources:
  Bucket:
    Type: AWS::S3::Bucket
    ExplodeMap: BucketMap
    Properties:
        BucketName: "!Explode Name"
```

## Author

[James Seward](https://github.com/jamesoff); AWS Solutions Architect, Amazon Web Services
