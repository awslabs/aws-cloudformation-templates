# How to install and use the Boto3 macro in your AWS account

The `Boto3` macro adds the ability to create CloudFormation resources that represent operations performed by [boto3](http://boto3.readthedocs.io/). Each `Boto3` resource represents one function call.

A typical use case for this macro might be, for example, to provide some basic configuration of resources.

## Deploying

1. You will need an S3 bucket to store the CloudFormation artifacts:
    * If you don't have one already, create one with `aws s3 mb s3://<bucket name>`

2. Package the CloudFormation template. The provided template uses [the AWS Serverless Application Model](https://aws.amazon.com/about-aws/whats-new/2016/11/introducing-the-aws-serverless-application-model/) so must be transformed before you can deploy it.

    ```shell
    aws cloudformation package \
        --template-file macro.template \
        --s3-bucket <your bucket name here> \
        --output-template-file packaged.template
    ```

3. Deploy the packaged CloudFormation template to a CloudFormation stack:

    ```shell
    aws cloudformation deploy \
        --stack-name boto3-macro \
        --template-file packaged.template \
        --capabilities CAPABILITY_IAM
    ```

4. To test out the macro's capabilities, try launching the provided example template:

    ```shell
    aws cloudformation deploy \
        --stack-name ExecutionRoleBuilderCFnMacro \
        --template-file ExecutionRoleBuilderCFnMacro.packaged.template  \
        --capabilities CAPABILITY_IAM
    ```

## Usage

To make use of the macro, add `Transform: Boto3` to the top level of your CloudFormation template.

Here is a trivial example template that adds a readme file to a new CodeCommit repository:

```yaml
Transform: Boto3
Resources:
  Repo:
    Type: AWS::CodeCommit::Repository
    Properties:
      RepositoryName: my-repo

  AddReadme:
    Type: Boto3::CodeCommit.put_file
    Mode: Create
    Properties:
      RepositoryName: !GetAtt Repo.Name
      BranchName: master
      FileContent: "Hello, world!"
      FilePath: README.md
      CommitMessage: Add a readme file
      Name: CloudFormation
```

## Features

### Resource type

The resource `Type` is used to identify a [boto3 client](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/clients.html) and the method of that client to execute.

The `Type` must start with `Boto3::` and be followed by the name of a client, a `.` and finally the name of a method.

The client name will be converted to lower case so that you can use resource names that look similar to other CloudFormation resource types.

Examples:
* `Boto3::CodeCommit.put_file`
* `Boto3::IAM.put_user_permissions_boundary`
* `Boto3::EC2.create_snapshot`

### Resource mode

The resource may contain a `Mode` property which specifies whether the boto3 call should be made on `Create`, `Update`, `Delete` or any combination of those.

The `Mode` may either be a string or a list of strings. For example:

* `Mode: Create`
* `Mode: Delete`
* `Mode: [Create, Update]`

### Resource properties

The `Properties` of the resource will be passed to the specified boto3 method as arguments. The name of each property will be modified so that it started with a lower-case character so that you can use property names that look similar to other CloudFormation resource properties.

### Controlling the order of execution

You can use the standard CloudFormation property `DependsOn` when you need to ensure that your `Boto3` resources are executed in the correct order.

## Examples


The following resource:

```yaml
ChangeBinaryTypes:
  Type: Boto3::CloudFormation.execute_change_set
  Mode: [Create, Update]
  Properties:
    ChangeSetName: !Ref ChangeSet
    StackName: !Ref Stack
```

will result in running the equivalent of the following:

```python
boto3.client("cloudformation").execute_change_set(changeSetName=<value of ChangeSet>, stackName=<value of StackName>)
```

when the stack is created or updated.

## Author

[Steve Engledow](https://linkedin.com/in/stilvoid)  
Senior Solutions Builder  
Amazon Web Services
