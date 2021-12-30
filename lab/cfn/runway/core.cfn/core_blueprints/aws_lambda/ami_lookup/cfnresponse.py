"""Vendored cfnresponse from AWS.

Retrieved from:
https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-function-code.html
Original copyright notice:

Copyright 2016 Amazon Web Services, Inc. or its affiliates.
All Rights Reserved.
This file is licensed to you under the AWS Customer Agreement (the "License").
You may not use this file except in compliance with the License.
A copy of the License is located at http://aws.amazon.com/agreement/ .
This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS
OF ANY KIND, express or implied.
See the License for the specific language governing permissions and limitations
under the License.
"""

import json

from botocore.vendored import requests

SUCCESS = "SUCCESS"
FAILED = "FAILED"


def send(event, context, responseStatus, responseData, physicalResourceId):  # noqa pylint: disable=C0103
    """Send response to CFN."""
    response_url = event['ResponseURL']

    print response_url

    response_body = {}
    response_body['Status'] = responseStatus
    response_body['Reason'] = ('See the details in CloudWatch Log Stream: ' +
                               context.log_stream_name)
    response_body['PhysicalResourceId'] = physicalResourceId or context.log_stream_name  # noqa
    response_body['StackId'] = event['StackId']
    response_body['RequestId'] = event['RequestId']
    response_body['LogicalResourceId'] = event['LogicalResourceId']
    response_body['Data'] = responseData

    json_response_body = json.dumps(response_body)

    print "Response body:\n" + json_response_body

    headers = {
        'content-type': '',
        'content-length': str(len(json_response_body))
    }

    try:
        response = requests.put(response_url,
                                data=json_response_body,
                                headers=headers)
        print "Status code: " + response.reason
    except Exception as e:  # pylint: disable=C0103,W0703
        print "send(..) failed executing requests.put(..): " + str(e)
