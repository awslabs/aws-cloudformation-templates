# CloudFormation Template: EC2, S3, RDS, CloudFront

This CloudFormation template allows you to create a basic infrastructure setup with Amazon EC2, Amazon S3, Amazon RDS, and Amazon CloudFront resources.

## Prerequisites

- AWS account with appropriate permissions to create and manage the required resources.
- AWS CLI or AWS Management Console for deploying the CloudFormation stack.

## Deployment Steps

1. Clone or download the CloudFormation template to your local machine.

2. Open a terminal or command prompt and navigate to the directory where the template is located.

3. Update the CloudFormation template (ResourceGenerator.yml) with your desired resource configurations. You can modify parameters like instance type, storage size, database engine, etc. to fit your requirements. Make sure to save the changes.

4. Deploy the stack using the AWS CLI or AWS Management Console:

   - AWS CLI:
        * run `aws cloudformation deploy --stack-name YourStackName --template-file ResourceGenerator.yml --parameter-overrides "DBPassword=YourDBPassword"`

   - AWS Management Console:
     - Sign in to the AWS Management Console.
     - Open the CloudFormation service.
     - Click on "Create stack" and select "Upload a template file".
     - Choose the modified template file (ResourceGenerator.yml) from your local machine.
     - Click on "Next" and follow the on-screen instructions to configure the stack options.
     - Review the stack details and click on "Create stack" to start the deployment.

5. Wait for the CloudFormation stack creation process to complete. You can monitor the progress in the AWS Management Console or by using the AWS CLI command:
   * run `aws cloudformation describe-stacks --stack-name YourStackName`

7. Before deleting the CloudFormation stack, it is recommended to ensure that there are no objects stored in the Amazon S3 bucket created by the stack. If the bucket contains objects, you must delete them before attempting to delete the stack. Otherwise, the stack deletion will fail because CloudFormation cannot delete a non-empty bucket.

   - To delete objects from the S3 bucket:

      -  Sign in to the AWS Management Console.
      -  Open the Amazon S3 service.
      -  Locate the bucket created by the CloudFormation stack.
      -  Select the bucket and navigate to the "Overview" tab.
      -  Delete all objects within the bucket by selecting them and clicking on the "Delete" button.
      -  Once all objects are deleted, you can proceed with deleting the CloudFormation stack.
      
 8.   You can Destroy cloudformation stack and it's resources in the AWS Management Console or by using the AWS CLI command as well:

   -  To delete the CloudFormation stack using AWS console:

      -  Sign in to the AWS Management Console.
      -  Open the CloudFormation service.
      -  Select the stack you want to delete (e.g., "YourStackName").
      -  Click on the "Delete" button.
      -  Confirm the stack deletion by clicking on "Yes, Delete".
      -  Wait for the stack deletion process to complete. 


   -  You can Destroy cloudformation stack and it's resources in the AWS Management Console or by using the AWS CLI command:
       * run `aws cloudformation delete-stack --stack-name YourStackName`
      
   -  You can monitor the progress in the AWS Management Console or by using the AWS CLI command:
      * run `aws cloudformation describe-stacks --stack-name YourStackName`

Once the stack deletion is successful, all the associated resources (EC2 instances, RDS instances, S3 bucket, CloudFront distribution) will be deleted, and you will have a clean state without any leftover resources.