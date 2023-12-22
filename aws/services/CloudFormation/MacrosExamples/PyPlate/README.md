# PyPlate

Run arbitrary python code in your CloudFormation templates

## Basic Usage

Place python code as a literal block anywhere in your template, the literal block will be replaced with the contents of
the `output` variable defined in your code. There are several variables available to your code:

params: dict containing the contents of the templateParameterValues
template: dict containing the entire template
account_id: AWS account ID
region: AWS Region

```yaml
AWSTemplateFormatVersion: "2010-09-09"
Description: tests String macro functions
Parameters:
  Tags:
    Default: "Env=Prod,Application=MyApp,BU=ModernisationTeam"
    Type: "CommaDelimitedList"
Resources:
  S3Bucket:
    Type: "AWS::S3::Bucket"
    Properties:
      Tags: |
        #!PyPlate
        output = []
        for tag in params['Tags']:
           key, value = tag.split('=')
           output.append({"Key": key, "Value": value})
Transform: [PyPlate]
```
## Advanced Usage - Querying AWS Services

It's possible to make boto3 calls in the python code block to retrieve information from AWS Services. 
When deploying PyPlate you can provide the ARN of an additional IAM Policy providing permissions for these calls.
Also you can increase the transform Lambda function's timeout from the default of 3 seconds; this won't
be enough for making API calls, at least 10 seconds is recommended.

Here's an example using PyPlate to build an application installer's name from template parameters, one of
which is an EC2 service lookup to get the CPU architecture being used, and making it available for reuse in
a Mapping value.

```yaml
AWSTemplateFormatVersion: '2010-09-09'
Transform: [PyPlate]
Parameters:
  AMI:
    Type: 'AWS::SSM::Parameter::Value<AWS::EC2::Image::Id>'
    Default: '/aws/service/ami-amazon-linux-latest/al2023-ami-kernel-6.1-arm64'
    Description: >-
      Path to AWS-managed SSM parameter that will resolve to the ID of the
      latest Amazon Linux 2023 AMI of the selected architecture.
  AppVersion:
    Type: String
    Description: Version of application to install
    Default: 8.7.1
Mappings:
  Value:
    SomeApplication:
      AppName: |
        #!PyPlate
        import boto3
        ec2 = boto3.client('ec2')
        response = ec2.describe_images(ImageIds=[params['AMI']])
        ami_architecture = response['Images'][0]['Architecture']
        output = ''.join((
          'some-application-',
          params['AppVersion'],
          '-linux-',
          ami_architecture 
        ))
```

## Author

[Jay McConnell](https://github.com/jaymccon)  
Partner Solutions Architect  
Amazon Web Services
