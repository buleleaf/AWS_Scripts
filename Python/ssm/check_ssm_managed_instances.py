import boto3
import json

client = boto3.client('ssm','us-west-2')

paginator = boto3.client('ssm').get_paginator('describe_instance_information')
page = paginator.paginate(
#   InstanceInformationFilterList=[
#     {
#       'key': 'PlatformTypes',
#       'valueSet': [
#         'Windows',
#       ],
#     },
#   ],
#   MaxResults=50,
)

# response = client.describe_instance_information(
#   InstanceInformationFilterList=[
#     {
#       'key': 'PlatformTypes',
#       'valueSet': [
#         'Windows',
#       ],
#     },
#   ],
#   MaxResults=50,
# )
instances = []
for response in page:
    for instanceinfo in response['InstanceInformationList']:
        if (instanceinfo['InstanceId']):
            instances.append(instanceinfo['InstanceId'])

print(instances)
