# How to install and use the Yaml2Json macro in your AWS account

The `Yaml2Json` macro translate a YAML element into its equivalent JSON code.
This is usefull for instance in cases of `AWS::CloudWatch::Dashboard` where the `DashboardBody` must be in JSON format, and your cloudformation template is in Yaml format

## Deploying

1. You will need an S3 bucket to store the CloudFormation artifacts:
    * If you don't have one already, create one with `aws s3 mb s3://<bucket name>`

2. Package the CloudFormation template. The provided template uses [the AWS Serverless Application Model](https://aws.amazon.com/about-aws/whats-new/2016/11/introducing-the-aws-serverless-application-model/) so must be transformed before you can deploy it.

    ```shell
    sam build
    ```

3. Deploy the packaged CloudFormation template to a CloudFormation stack:

    ```shell
    sam deploy --stack-name Yaml2Json --capabilities CAPABILITY_IAM
    ```

4. To test out the macro's capabilities, try launching the provided example template:

    ```shell
    aws cloudformation deploy \
        --stack-name Yaml2Json-example \
        --template-file template-example.yaml \
        --capabilities CAPABILITY_IAM
    ```

## Usage

To make use of the macro, add `Transform: Yaml2Json` to the top level of your CloudFormation template.

Here is a trivial example template:

```yaml
AWSTemplateFormatVersion: '2010-09-09'
Transform: 
  - Yaml2Json
Resources:
  Dashboard: 
    Type: AWS::CloudWatch::Dashboard
    Properties:
      DashboardName: 
        Fn::Sub: '${AWS::StackName}'
      DashboardBody: 
        Fn::Yaml2Json:
          widgets:
            - type: text
              x: 0
              y: 0
              width: 9
              height: 9
              properties:
                markdown: "# This Dashboard illustrate the `Yaml2Json` Macro\n"
```

## Features

* Convert a YAML element into a JSON element with the pseudo intrinsic function "Fn::Yaml2Json"

## Author

[Julien Masnada](https://www.linkedin.com/in/julienmasnada)  

