import boto3

client = boto3.client('iam', 'us-west-2')

response = client.list_roles()

# print(response)
for role in response['Roles']:
    print(role['RoleName'])
