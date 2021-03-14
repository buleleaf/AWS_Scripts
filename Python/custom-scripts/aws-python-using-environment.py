import boto3
import os

# this will use the temporary token
ec2client = boto3.client('ec2')

current_region = os.environ['AWS_DEFAULT_REGION']
ACCOUNT_ID = boto3.client('sts').get_caller_identity().get('Account')
