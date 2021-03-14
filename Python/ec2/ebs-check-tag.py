import boto3
import os

region = 'us-west-2'

ec2client = boto3.client('ec2', region_name=region)

response = ec2client.describe_instances(
	Filters=[
		{
		'Name': 'tag:StatelessHa',
		'Values': ['yes']
		}
	]
)

print(response)