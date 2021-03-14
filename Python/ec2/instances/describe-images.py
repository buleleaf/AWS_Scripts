import boto3
from botocore.exceptions import ClientError
import csv

client = boto3.client('ec2', region_name='us-west-2')

response = client.describe_images(
	Owners=[
		'776141660684'
	]
	)

print(response)