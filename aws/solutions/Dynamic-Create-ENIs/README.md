# How can I create or add a variable number of resources to an AWS CloudFormation stack?

## Summary
You have a variable amount of input in your stack and want to create a new Resource, or add that amount to a Resource.

## Issue
How can I create or add a variable or unknown number of resources to an AWS CloudFormation stack?

 ## Short Description
AWS CloudFormation supports the Fn::Select function for getting a value out of a list of objects. However, the function does not work in use cases where the number of objects is unknown. For example, the number of objects is unknown in a list of IP addresses for an AWS WAF IPSet or a list of strings that need a resource created for each string.

Note: The Fn::Select function currently does not provide an elastic network interface (ENI) ID for the resources generated  when a stack is created, updated, or deleted. For more information on the functions supported by AWS, see Intrinsic Function Reference and  Condition Functions.

## Resolution
Update the Parameters section of your AWS CloudFormation template

For the numberList parameter, enter a list of your IP addresses for the CommaDelimitedList property. 
For the subnet parameter, choose a subnet that matches your list of IP addresses to specify where to create the ENIs. 
For the security parameter, choose a security group in the same VPC as the subnets.
Save the changes you made to your template.