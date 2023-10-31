# Copyright 2018 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You
# may not use this file except in compliance with the License. A copy of
# the License is located at
#
#     http://aws.amazon.com/apache2.0/
#
# or in the "license" file accompanying this file. This file is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
# ANY KIND, either express or implied. See the License for the specific
# language governing permissions and limitations under the License.

from urllib2 import build_opener, HTTPHandler, Request
import base64
import boto3
import httplib
import json

def sendResponse(event, context, status, message):
    body = json.dumps({
        "Status": status,
        "Reason": message,
        "StackId": event['StackId'],
        "RequestId": event['RequestId'],
        "LogicalResourceId": event['LogicalResourceId'],
        "PhysicalResourceId": event["ResourceProperties"]["Action"],
        "Data": {},
    })

    request = Request(event['ResponseURL'], data=body)
    request.add_header('Content-Type', '')
    request.add_header('Content-Length', len(body))
    request.get_method = lambda: 'PUT'

    opener = build_opener(HTTPHandler)
    response = opener.open(request)

def execute(action, properties):
    action = action.split(".")

    if len(action) != 2:
        return "FAILED", "Invalid boto3 call: {}".format(".".join(action))

    client, function = action[0], action[1]

    try:
        client = boto3.client(client.lower())
    except Exception as e:
        return "FAILED", "boto3 error: {}".format(e)

    try:
        function = getattr(client, function)
    except Exception as e:
        return "FAILED", "boto3 error: {}".format(e)

    properties = {
        key[0] + key[1:]: value
        for key, value in properties.items()
    }

    try:
        function(**properties)
    except Exception as e:
        return "FAILED", "boto3 error: {}".format(e)

    return "SUCCESS", "Completed successfully"

def handler(event, context):
    print("Received request:", json.dumps(event, indent=4))

    request = event["RequestType"]
    properties = event["ResourceProperties"]

    if any(prop not in properties for prop in ("Action", "Properties")):
        print("Bad properties", properties)
        return sendResponse(event, context, "FAILED", "Missing required parameters")

    mode = properties["Mode"]

    if request == mode or request in mode:
        status, message = execute(properties["Action"], properties["Properties"])
        return sendResponse(event, context, status, message)

    return sendResponse(event, context, "SUCCESS", "No action taken")
