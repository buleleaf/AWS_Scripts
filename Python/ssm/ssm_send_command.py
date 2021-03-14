import boto3
import json
import csv

instance = 'i-0f16f37a12eb06c76'

command_id = '315c41c9-8a0c-45f6-9061-7657ef979945'

client = boto3.client('ssm','us-west-2')

with open('/Users/dmansfield/lab/aws/python/ssm/instances.csv', 'r') as f:
	reader = csv.reader(f)
	instances = list(reader)

for instance in instances:
    for i in instance:
        print(i)

        client.send_command(
            InstanceIds=[i],
            DocumentName='CloudWatchAgentInstallAndConfigure'
        )

# response = client.send_command(
#     InstanceIds=[instance],
#     DocumentName='CloudWatchAgentInstallAndConfigure'
# )

# command_id = response['Command']['CommandId']
# print(command_id)