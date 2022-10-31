# BlockCopier CloudFormation Macro

The `BlockCopier` macro provides a template-wide `BlockCopier` property for CloudFormation resources. It allows you to copy blocks of content from any location in the template to be used elsewhere in the same template. 
Whilst copying is it is possible to replace values in the original block using a mapping table.

## How to install and use the BlockCopier macro in your AWS account

### Deploying

1. You will need an S3 bucket to store the CloudFormation artifacts:
    * If you don't have one already, create one with `aws s3 mb s3://<bucket name>`

2. Package the Macro CloudFormation template. The provided template uses [the AWS Serverless Application Model](https://aws.amazon.com/about-aws/whats-new/2016/11/introducing-the-aws-serverless-application-model/) so must be transformed before you can deploy it.

    ```shell
    aws cloudformation package \
        --template-file template.yaml \
        --s3-bucket <your bucket name here> \
        --output-template-file packaged.yaml
    ```

3. Deploy the packaged CloudFormation template to a CloudFormation stack:

    ```shell
    aws cloudformation deploy \
        --stack-name BlockCopier-macro \
        --template-file packaged.yaml \
        --capabilities CAPABILITY_IAM
    ```

4. To test out the macro's capabilities, try launching the provided example template:

    ```shell
    aws cloudformation deploy \
        --stack-name BlockCopier-test \
        --template-file test.yaml \
        --capabilities CAPABILITY_IAM
    ```

### Usage

Once the macro has been deployed, to make use of it add `Transform: BlockCopier` to the top level of your CloudFormation template.

At the location where you want the copied block to be inserted, specify the `BlockCopier` section.
You then specify the path to the original block in the template file using [JSON path](https://github.com/h2non/jsonpath-ng) notation.
NOTE: The BlockCopier section will be removed once the template has been processed.

### Properties
#### Path (Required)

```Path``` contains the path of the block to copy using [JSON path](https://github.com/h2non/jsonpath-ng) notation.
NOTE: Even if the template is written using YAML, it is necessary to use JSON path notation to identify the souce block because CloudFormation transforms your template to JSON before executing the Macro.

#### Replacements (Optional)

```Replacements``` section contains a map of values to replace when copying the block from the original location.

### Example

```yaml
AWSTemplateFormatVersion: '2010-09-09'
Transform:
  - BlockCopier
Resources:
  BucketWithTags:
    Type: AWS::S3::Bucket
    Properties:
      Tags:
        - Key: Bucket Name
          Value: BucketOne
        - Key: Username
          Value: Test user one
        - Key: Another string to change
          Value: Part or all of this string can be changed to a different value
  BucketWithoutTags:
    Type: AWS::S3::Bucket
    Properties:
      Tags:
         BlockCopier: 
            Path: $.Resources.BucketWithTags.Properties.Tags
            Replacements:
              - Original: BucketOne
                Replacement: BucketTwo
              - Original: Test user one
                Replacement: Test user two
              - Original: or all of this string can be
                Replacement: of this string has been
```
#### Explanation

This example will copy the block with the JSON path ```$.Resources.BucketWithTags.Properties.Tags``` to the destination where the ```BlockCopier``` section is. 

### Processed Template

Using this example, the processed template will result become (note this has been converted from JSON for reference, processed temlates will always be in JSON format)

```yaml
AWSTemplateFormatVersion: 2010-09-09
Resources:
  BucketWithTags:
    Type: 'AWS::S3::Bucket'
    Properties:
      Tags:
        - Key: Bucket Name
          Value: BucketOne
        - Key: Username
          Value: Test user one
        - Key: Another string to change
          Value: Part or all of this string can be changed to a different value
  BucketWithoutTags:
    Type: 'AWS::S3::Bucket'
    Properties:
      Tags:
        - Key: Bucket Name
          Value: BucketTwo
        - Key: Username
          Value: Test user two
        - Key: Another string to change
          Value: Part of this string has been changed to a different value
```

### Important - Naming resources

You cannot use BlockCopier on resources that use a hardcoded name (`Name:` property). Duplicate names will cause a CloudFormation runtime failure.
If you wish to use BlockCopier for blocks containing a name (or other resources that must be unique) ensure you use the ```Replacements``` section as described earlier.

## Author

[Carl Reid](https://twitter.com/tek_carl)

