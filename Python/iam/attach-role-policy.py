import csv
import boto3
import pprint

client = boto3.client('iam')

with open('roles.csv', 'r') as f:
	reader = csv.reader(f)
	iam_roles = list(reader)


for roles in iam_roles:
    for role in roles:
        # print(role)
        client.attach_role_policy(
            RoleName=role,
            PolicyArn='arn:aws:iam::229074042392:policy/TagKeyEnforcement-Ec2'
        )
        print(role)