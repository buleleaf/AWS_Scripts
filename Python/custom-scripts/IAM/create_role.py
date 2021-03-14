import boto3
import json

region = 'ap-northeast-1'

iam_client = boto3.client('iam', region_name=region)

response = iam_client.create_role(
    RoleName='EdwardsEC2RoleforSSMandCWAgent',
    Description='',
    AssumeRolePolicyDocument={
        'Version': '2012-10-17',
        'Statement': [
            {
                'Effect': 'Allow',
                'Action': [
                    'sts:AssumeRole'
                ],
                'Principal': {
                    'Service': [
                        'ec2.amazonaws.com'
                    ]
                }
            }
        ]
    }
)
response = iam_client.create_instance_profile(
    InstanceProfileName='EdwardsEC2RoleforSSMandCWAgent'
)
response = iam_client.attach_role_policy(
    RoleName='EdwardsEC2RoleforSSMandCWAgent',
    PolicyArn='arn:aws:iam::aws:policy/service-role/AmazonSSMMaintenanceWindowRole'
)
response = iam_client.attach_role_policy(
    RoleName='EdwardsEC2RoleforSSMandCWAgent',
    PolicyArn='arn:aws:iam::607180602984:policy/EdwardsEC2RoleforSSMandCWAgent'
)
response = iam_client.list_policies()