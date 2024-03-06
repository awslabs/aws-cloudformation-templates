# API Gateway RESTAPI with Lambda Non-Proxy Integration

Use this template to create a sample API Gateway with lambda non-proxy integration

#### Lambda Function

The Lambda function used is simple it parses the input event object for the name,
city, time and day properties. It returns a greeting message as a JSON object. 

#### API Gateway
Method request payload

```json
{
  "$schema": "http://json-schema.org/draft-04/schema#",
  "title": "GetStartedLambdaIntegrationInputModel",
  "type": "object",
  "properties": {
    "callerName": { "type": "string" }
  }
}
```

Request Parameters
```json
 {
   "method.request.path.city": "true",
   "method.request.querystring.time": "true",
   "method.request.header.day": "true"
 }
```
Request Mapping Template

```json
#set($inputRoot = $input.path('$'))
{
  "city": "$input.params('city')",
  "time": "$input.params('time')",
  "day":  "$input.params('day')",
  "name": "$inputRoot.callerName"
}
```
#### Test the REST API

To test the RESTAPI
1) In Method exectuion, choose `Test`
2) choose `POST` from method drop-down list
3) In path, type `Boston`
4) In Query Strings, type `time=morning`
5) In Headers, type `day:Tuesday`
6) In Request Body, type `{"callerName":"Bob"}`
7) Choose Test
8) Verify the return response as follows:

``````````{ Good morning, Bob of Boston. Happy Tuesday``````````
