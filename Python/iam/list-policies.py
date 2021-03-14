import boto3

client = boto3.client('iam')

response = client.list_policies(
    Scope='Local',
    # OnlyAttached=False,
)

for policy in response['Policies']:
    if policy['AttachmentCount'] == 0:
        print(policy['PolicyName'])