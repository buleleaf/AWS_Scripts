import json
import boto3

oregon = 'us-west-2'
frankfurt = 'eu-central-1'
singapore = 'ap-southeast-1'
tokyo = 'ap-northeast-1'
virginia = 'us-east-1'

client = boto3.client('ec2', region_name=virginia)

response = client.describe_vpcs()

print(json.dumps(response, indent=4, sort_keys=True))

response = client.describe_subnets()

print(json.dumps(response, indent=4, sort_keys=True))