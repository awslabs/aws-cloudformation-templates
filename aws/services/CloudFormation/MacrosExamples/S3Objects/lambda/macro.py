# Copyright 2018-2021 Amazon.com, Inc. or its affiliates. All Rights Reserved.
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

import boto3
import os

LAMBDA_ARN = os.environ["LAMBDA_ARN"]

s3_client = boto3.client("s3")


def handle_template(request_id, template):
    new_resources = {}

    for name, resource in list(template.get("Resources", {}).items()):
        if resource["Type"] == "AWS::S3::Object":
            props = resource["Properties"]

            if (
                len(
                    [
                        prop
                        for prop in resource["Properties"]
                        if prop in ["Body", "URL", "Base64Body", "Source"]
                    ]
                )
                != 1
            ):
                raise Exception(
                    "You must specify exactly one of: Body, URL, Base64Body, Source"
                )

            target = props["Target"]

            if "ACL" not in target:
                target["ACL"] = "private"

            resource_props = {
                "ServiceToken": LAMBDA_ARN,
                "Target": target,
            }

            if "Body" in props:
                resource_props["Body"] = props["Body"]

            elif "URL" in props:
                resource_props["URL"] = props["URL"]

            elif "Base64Body" in props:
                resource_props["Base64Body"] = props["Base64Body"]

            elif "Source" in props:
                resource_props["Source"] = props["Source"]

            new_resources[name] = {
                "Type": "Custom::S3Object",
                "Version": "1.0",
                "Properties": resource_props,
            }

    for name, resource in list(new_resources.items()):
        template["Resources"][name] = resource

    return template


def handler(event, context):
    try:
        template = handle_template(event["requestId"], event["fragment"])
    except Exception as e:
        return {
            "requestId": event["requestId"],
            "status": "failure",
            "errorMessage": str(e),
            "fragment": event["fragment"],
        }

    return {
        "requestId": event["requestId"],
        "status": "success",
        "fragment": template,
    }
