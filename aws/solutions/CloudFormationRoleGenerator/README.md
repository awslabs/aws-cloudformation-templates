# CloudFormationRoleGenerator

This solution allows you to generate a IAM Role used to specifically create / update / delete a stack.
When developing a new stack with CloudFormation it is sometime complicated to figure out what permissions would a CI/CD pipeline need in odrer maintain a stack. 
The easy solution of associating administrtive priviledges to the pipeline is not a satisfactory solution. 
Instead it is better to restrict the pipeline priviledges to the ones strictly necesary for that specific stack.

This solution consist in three steps:

1. Create a StackDeveloper Role, and give is administrative prividleges
1. Create a CloudTrail trail and filter on this specific user.
1. After the stack development is complete, stop the trail and generate role acordingly.

You can then associate the role to the user / group that would be in charge of maintaining the stack

# Create a StackDeveloper User

You first need to create the `StackDeveloper` and configure your AWS Cli to use that newly created user

## Creating the user

```bash
sam build --template template-iam.yaml
sam deploy --guided --stack-name CloudFormationRoleGeneratorStackDeveloper --capabilities "CAPABILITY_IAM CAPABILITY_NAMED_IAM"
```

## Configuring the AWS CLi

```bash
aws configure set profile.StackDeveloper.region eu-west-1
aws configure set profile.StackDeveloper.aws_access_key_id <AccessKeyId>
aws configure set profile.StackDeveloper.aws_secret_access_key <SecretAccessKey>
```

# Develop your stack

## Start logging
With the new user created it is now possible to start logging.

```bash
aws cloudtrail start-logging --name <Trail>
``` 

## Create / develop / delete your stack
You can the create, develop, and delete your stack. The delete is important in order to have a full cycle for the role

```bash
sam build --template template-stack.yaml
sam deploy --profile "StackDeveloper" --guided --stack-name CloudFormationRoleGeneratorSampleStack
aws cloudformation --profile "StackDeveloper" delete-stack --stack-name CloudFormationRoleGeneratorSampleStack
```

## Stop logging

Finally you can stop logging 

```bash
aws cloudtrail stop-logging --name <Trail>
```

# Generate the IAM policy necessary to update the stack

```shell
aws s3 cp --recursive s3://<Bucket>/AWSLogs/<AccountId>/CloudTrail/<Region>/<YYYY>/<MM>/<DD> /path/to/logs
./generate_policy.py --logs-dir /path/to/logs --validate 
```

## Cleanup

To delete the stacks that you created, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:

```bash
aws cloudformation delete-stack --stack-name CloudFormationRoleGeneratorSampleStack
aws cloudformation delete-stack --stack-name CloudFormationRoleGeneratorStackDeveloper
```