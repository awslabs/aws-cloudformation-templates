# VPC Main/Default Route Table Lookup Custom Resource

This custom resource returns the main/default Route Table ID of the VPC that is created as part of the CloudFormation template.

When a VPC is created, a respective route table will be created for the VPC. When a VPC is created using CloudFormation, the main/default Route Table ID is required to add routes to the Route Table. This custom resource can be used to retrieve the main Route Table ID which can be used in updating/modifying the routes in later resources of the stack.

## Running the example

### 1. Download the sample Lambda function and CloudFormation template

Download the RouteTable.template and Routetable.py files to your local directory.

### 2. Create a zip file for Lambda function and store it in S3 bucket

Zip the Routetable.py file to create Routetable.zip file. Make sure that the Routetable.py is located at the root level of the zip file as shown below.

```console
-> Routetable.zip
    |
    |-> Routetable.py
```

Upload the Routetable.zip in an S3 bucket in your account. Make sure that the S3 bucket should be in the same region in which the CloudFormation stack will be launched in next step. Below AWS CLI command can be used to upload the zip file to S3 bucket.

```console
aws s3 cp <path-to-zip-file>/Routetable.zip s3://<s3-bucket-name>/Routetable.zip
```

### 3. Launch CloudFormation stack using RouteTable.template file

Launch CloudFormation stack by passing "Bucket-Name" in which Lambda zip file is uploaded, Zip file name (say Routetable.zip) and the Lambda file name inside zip (Routetable) as parameters. Below AWS CLI command can be used to launch stack.

```console
aws cloudformation create-stack --stack-name myvpcstack --template-body file://RouteTable.template --parameters ParameterKey=Bucket,ParameterValue=<S3-Bucket-Name> ParameterKey=Key,ParameterValue=Routetable.zip ParameterKey=Lambdahandler,ParameterValue=Routetable --capabilities CAPABILITY_NAMED_IAM --region <region>
```

The above example stack will create a VPC and uses custom resource to fetch the main Route Table ID and then add a public route to main Route Table of the VPC. Outputs section of the stack will display the Route Table ID.
