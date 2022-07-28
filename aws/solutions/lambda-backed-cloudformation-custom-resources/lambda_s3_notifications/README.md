# Use existing S3 bucket for Lambda notifications using CloudFormation

As of now, CloudFormation only supports creating Notification Configurations to those S3 buckets which are created using CloudFormation. Since a separate resource for adding Notification Configuration to S3 bucket is not available, We have to either create "AWS::S3::Bucket" resource using CloudFormation to which notification configuration is added using "NotificationConfiguration" property or add it manually to an existing bucket.

In order to use CloudFormation to add NotificationConfiguration to an existing S3 bucket, you can use Lambda backed Custom resources where a Lambda function is triggered by CloudFormation which in turn triggers PutBucketNotification API call to add notification configuration to an existing S3 bucket.

This solution provides complete Lambda code and CloudFormation template which uses an existing S3 Bucket for creation of Lambda notifications using CloudFormation.

## Running the example

### 1. Download the sample Lambda function and CloudFormation template

Download the LambdaS3.template and LambdaS3.py files to your local directory.

### 2. Create a zip file for Lambda function and store it in S3 bucket

Zip the LambdaS3.py file to create LambdaS3.zip file. Make sure that the LambdaS3.py is located at the root level of the zip file as shown below.

```console
-> LambdaS3.zip
    |
    |-> LambdaS3.py
```

Upload the LambdaS3.zip in an S3 bucket in your account. Make sure that the S3 bucket should be in the same region in which the CloudFormation stack will be launched in next step. Below AWS CLI command can be used to upload the zip file to S3 bucket.

```console
aws s3 cp <path-to-zip-file>/LambdaS3.zip s3://<s3-bucket-name>/LambdaS3.zip
```

### 3. Launch CloudFormation stack using LambdaS3.template file

Launch CloudFormation stack by passing "Existing-Bucket-Name" which is used for Lambda notifications, "Bucket-Name" in which Lambda zip file is uploaded, Zip file name (say LambdaS3.zip) and the Lambda file name inside zip (LambdaS3) as parameters. Below AWS CLI command can be used to launch stack.

```console
aws cloudformation create-stack --stack-name lambda-s3-notification --template-body file://LambdaS3.template --parameters ParameterKey=NotificationBucket,ParameterValue=<existing-bucket-for-lambda-notification> ParameterKey=LambdaCodeBucket,ParameterValue=<s3-bucket-with-lambda-zip-file> ParameterKey=Lambdahandler,ParameterValue=LambdaS3 ParameterKey=LambdaCodeKey,ParameterValue=LambdaS3.zip --capabilities CAPABILITY_NAMED_IAM --region <region>
```

The above example stack will create a lambda function to which notifications should be configured, lambda permission for S3 and will add required notification configuration to the existing S3 bucket.
