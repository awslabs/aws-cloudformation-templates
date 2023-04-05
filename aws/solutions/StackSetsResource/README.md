# StackSetsResource

----

## Built-in Stack Set Resource 

Before you use the custom resource in this repository, see the AWS CloudFormation [AWS::CloudFormation::StackSet](https://docs.aws.amazon.com/en_us/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-stackset.html) resource.  This built-in resource was made available in September, 2020.

----

AWS CloudFormation Lambda-backed Custom Resource for launching StackSets.

The lambda function is written in Python and based on the  [crhelper.py](https://github.com/awslabs/aws-cloudformation-templates/tree/master/community/custom_resources/python_custom_resource_helper) Custom Resource framework.

* `FunctionCode` contains the lambda function and helper libraries.
* `Templates` contains the function deploy templateÂ and a sample StackSet resource.

## Install

### Using the aws cli:

You can install the function using the CloudFormation [`package`](https://docs.aws.amazon.com/cli/latest/reference/cloudformation/package.html) and [`deploy`](https://docs.aws.amazon.com/cli/latest/reference/cloudformation/deploy/index.html) commands.
You will need an S3 bucket to store the lambda function code.  Once you've created the bucket,
 run the following CLI commands to create the function stack:

```
aws cloudformation package \
  --template-file Templates/stackset-function-template.yaml \
  --s3-bucket *Your S3 bucket* \
  --s3-prefix *Your S3 object prefix* \
  --output-template-file Templates/packaged-stackset-function-template.yaml
```

```
aws cloudformation deploy \
  --template-file Templates/packaged-stackset-function-template.yaml \
  --stack-name StackSetCustomResource \
  --capabilities CAPABILITY_IAM
```

Alternatively, if you'd like to override one or more of the function stack template parameters:

```
aws cloudformation deploy \
  --template-file Templates/packaged-stackset-function-template.yaml \
  --stack-name StackSetCustomResource \
  --parameter-overrides RoleName=custom-resource-stacksets RolePath=/company/ \
  --capabilities CAPABILITY_IAM
```

CloudFormation will package up the python files, upload them to your S3 bucket, create the lambda function with appropriate permissions and export the Lambda function ARN as `StackSetCustomResource` for use in other stacks.


## Sample CloudFormation snippet:

The following YAML snippet demonstrates how to define a StackSet within your template using the exported ARN of the lambda function:

```yaml
Resources:
  StackSet:
    Type: Custom::StackSet
    Properties:
      ServiceToken:
        Fn::ImportValue: StackSetCustomResource
      StackSetName: EventDynamoDB
      StackSetDescription: Deploy DynamoDB for event tables in dev and production
      TemplateURL: https://s3.us-east-2.amazonaws.com/cloudformation-pipeline/events.yaml
      Parameters:
        - ReadCapacity: 20
        - WriteCapacity: 20
      Capabilities: !Ref "AWSS::NoValue"
      AdministrationRoleARN: MyStackSetAdministrationRoleARN
      ExecutionRoleName: MyStackSetExecutionRoleName
      OperationPreferences: {
        "RegionOrder": , [ "us-east-2", "us-west-2" ]
        "FailureToleranceCount": 0,
        "MaxConcurrentCount": 3
      }
      Tags:
        - Environment: Testing
        - Creator: Chuck
      StackInstances:
        # Dev
        - Regions:
            - us-east-2
          Accounts:
            - XXXXXXXXXXXX
        # Production
        - Regions:
            - us-east-2
            - us-west-2
          Accounts:
            - YYYYYYYYYYYY
          ParameterOverrides:
            - ReadCapacity: 50
            - WriteCapacity: 50
```

## ToDo
```
[ ] Support retaining stacks on delete
[ ] Support account gate functions
```
