# Date functions

Provides date tranformation utility functions. Can be used in things like policies that need ISO formatted date values.

## Basic Usage

Place the transform where you would like the output to be placed and provide the [parameters](#parameters) for the [operation](#available-operations) you have
chosen.

```yaml
Parameters:
  Date:
    Default: "This is a date"
    Type: String
    AllowedPattern: "^$|^\\d{4}(-\\d\\d(-\\d\\d(T\\d\\d:\\d\\d(:\\d\\d)?(\\.\\d+)?(([+-]\\d\\d:\\d\\d)|Z)?)?)?)?$"
Resources:
  S3Bucket:
    Type: "AWS::S3::Bucket"
    Properties:
      Tags:
        - Key: Date
          Value:
            'Fn::Transform':
             - Name: 'Date'
               Parameters:
                 Date: !Ref Date
                 Operation: Current
```
The original use case for this was to create an SSM parameter with an expiration date, which is exemplified in the 
following snippet:
```yaml
  # Secret key SSM paramber
  S3UserSecretAccessKey:
    Type: "AWS::SSM::Parameter"
    Properties:
      Name: !Sub "/S3Bucket/API/Secret/${S3Bucket}"
      Type: "String" # This really should be a SecureString, but CloudFormation doesn't yet support it for some reason
      Value: !GetAtt S3AccessKey.SecretAccessKey
      Description: "SSM Parameter for S3Bucket Secret"
      Tier: Advanced
      Policies:
        Fn::Sub:
          - "[{ \"Type\":\"Expiration\",\"Version\":\"1.0\",\"Attributes\": {\"Timestamp\":\"${ExpireDate}\" } }]"
          - ExpireDate:
              Fn::Transform:
                - Name: 'Date'
                  # Have the date be 30 days from now...
                  Parameters:
                    # No Date passed in means we add the days to now()
                    Days: !Ref DaysToExpiration
                    Operation: "Add"

```
The `Fn::Transform` will place a value in the expiration policy for the above parameter that will expire based on the 
`DaysToExpiration` parameter (From the `Parameters` section of the CloudFormation template). 

## Parameters

| Name | Description | Format |
|------|-------------|--------|
| [Date](#date) | Date to use (defaults to `now`) | ISO Date |
| [Date2](#date2) | Date to use for [`Days`](#days) operation (also defaults to `now`) | ISO Date |
| [Days](#days) | Number of days to add or subtract in the [`Add`](#add) or [`Subtract`](#subtract] operations | Integer |

## Date

This parameter is used in the [`Current`](#current), [`Add`](#add), and [`Subtract`](#subtract) operations.

It should be an ISO formatted date, and will default to the current date if it is empty or not passed.

## Date2

This parameter is also used in the [`Current`](#current), [`Add`](#add), and [`Subtract`](#subtract) operations.

It should be an ISO formatted date, and will default to the current date if it is empty or not passed.

## Days

This parameter is used in the [`Add`](#add), and [`Subtract`](#subtract) operations.

It should be an integer, if it is omitted, it defaults to zero (`0`)

## Available Operations

| Name | Description | Parameters |
|------|-------------|------------|
| [Current](#current) | Returns the current date (or value of the [`Date`](#date) parameter | [`Date`](#date) (optional) |
| [Add](#add) | Adds number of days to the [`Date`](#date) | [`Date`](#date) defaults to `now()`, [`Days`](#days-1) defaults to `0` |
| [Subtract](#subtract) | Subtracts number of days from the [`Date`](#date) | `Date` defaults to `now()`, [`Days`](#days-1) defaults to `0` |
| [Days](#days-1) | Returns the number of days from between two dates | [`Date`](#date) defaults to `now()`, [`Date2`](#date2) defaults to `now()` |

### Current

Returns a copy of the current date and time in ISO format
 
### Add

Adds the [`Days`](#days) parameter value to the `Date` value.

### Subtract

Subtracts the  [`Days`](#days) from the [`Date`](#date)

### Days

Calculates the number of days between [`Date`](#date) and [`Date2`](#date2)

