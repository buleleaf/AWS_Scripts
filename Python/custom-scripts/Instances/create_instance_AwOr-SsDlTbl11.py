import boto3
import time
from collections import defaultdict

region = 'us-west-2'
ami_id = 'ami-0f9cc35d712b86a4f'
keyname = 'aws-corpinfo-msp'
instance_type = 'm5d.4xlarge'

# Shared Services VPC
subnet_id = 'subnet-584fb32e'
sg_1 = 'sg-85375fe3'
sg_2 = 'sg-ed08608b'
sg_3 = 'sg-c00961a6'

# IAM ROLE
iam_role = 'EdwardsEC2RoleforSSMandCWAgent'

# EBS
root_drive = '/dev/sda1'
root_drive_size = 80
root_drive_type = 'gp2'

second_drive = 'xvdb'
second_drive_size = 100
second_drive_type = 'gp2'

ec2 = boto3.client('ec2', region_name=region)


instance = ec2.run_instances(
    ImageId=ami_id,
    MinCount=1,
    MaxCount=1,
    InstanceType=instance_type,
    BlockDeviceMappings=[
        {
            'DeviceName': root_drive,
            'Ebs': {
                'VolumeSize': root_drive_size,
                'VolumeType': root_drive_type,
                'Encrypted': True,

            },
        },
        {
            'DeviceName': second_drive,
            'Ebs': {
                'VolumeSize': second_drive_size,
                'VolumeType': second_drive_type,
                'Encrypted': True,

            },
        },
    ],
    KeyName=keyname,
    IamInstanceProfile={
        'Arn': 'arn:aws:iam::590992000271:instance-profile/EdwardsEC2RoleforSSMandCWAgent'
    },
    NetworkInterfaces=[
        {
            'AssociatePublicIpAddress': False,
            'DeviceIndex': 0,
            'SubnetId': subnet_id,
            'Groups': [
                sg_1,
                sg_2,
                sg_3,
            ]

        }
    ],
    TagSpecifications=[
        {
            'ResourceType': 'instance',
            'Tags': [
                {
                    "Key": "Application",
                    "Value": "DataLakes.Tableau"
                },
                {
                    "Key": "Purpose",
                    "Value": "Visualization and Reporting"
                },
                {
                    "Key": "ApplicationTier",
                    "Value": "Application"
                },
                {
                    "Key": "ApplicationTierLevel",
                    "Value": "No Tier"
                },
                {
                    "Key": "Managed",
                    "Value": "Yes"
                },
                {
                    "Key": "Environment",
                    "Value": "Test"
                },
                {
                    "Key": "Name",
                    "Value": "AwOr-SsDlTbl11"
                },
                {
                    "Key": "CorpInfoMSP:TakeNightlySnapshot",
                    "Value": "Yes"
                },
                {
                    "Key": "MonitoredServices",
                    "Value": "Yes"
                },
                {
                    "Key": "RequestNumber",
                    "Value": "RITM00"
                },
                {
                    "Key": "OperationHours",
                    "Value": "9x5"
                },
                {
                    "Key": "CostCenter",
                    "Value": "1001798953.63055552 (next year 1001798855)"
                },
                {
                    "Key": "ServiceLocation",
                    "Value": "Global"
                },
                {
                    "Key": "ServiceOwner",
                    "Value": "Barb Latulippe"
                },
                {
                    "Key": "TechnicalOwner",
                    "Value": "Pablo Vivanco"
                },
                {
                    "Key": "ContactPreference",
                    "Value": "Email"
                },
                {
                    "Key": "PatchGroup",
                    "Value": "PilotAutoReboot"
                },
                {
                    "Key": "Schedule",
                    "Value": "Irvine-Business-Hours:M-F from 8:00AM to 6:00PM (GMT-7/8)"
                },
                {
                    "Key": "Validated",
                    "Value": "No"
                }
            ]
        },
        {
            'ResourceType': 'volume',
            'Tags': [
                {
                    "Key": "Application",
                    "Value": "DataLakes.Tableau"
                },
                {
                    "Key": "Purpose",
                    "Value": "Visualization and Reporting"
                },
                {
                    "Key": "ApplicationTier",
                    "Value": "Application"
                },
                {
                    "Key": "ApplicationTierLevel",
                    "Value": "No Tier"
                },
                {
                    "Key": "Managed",
                    "Value": "Yes"
                },
                {
                    "Key": "Environment",
                    "Value": "Test"
                },
                {
                    "Key": "Name",
                    "Value": "AwOr-SsDlTbl11"
                },
                {
                    "Key": "CorpInfoMSP:TakeNightlySnapshot",
                    "Value": "Yes"
                },
                {
                    "Key": "MonitoredServices",
                    "Value": "Yes"
                },
                {
                    "Key": "RequestNumber",
                    "Value": "RITM00"
                },
                {
                    "Key": "OperationHours",
                    "Value": "9x5"
                },
                {
                    "Key": "CostCenter",
                    "Value": "1001798953.63055552 (next year 1001798855)"
                },
                {
                    "Key": "ServiceLocation",
                    "Value": "Global"
                },
                {
                    "Key": "ServiceOwner",
                    "Value": "Barb Latulippe"
                },
                {
                    "Key": "TechnicalOwner",
                    "Value": "Pablo Vivanco"
                },
                {
                    "Key": "ContactPreference",
                    "Value": "Email"
                },
                {
                    "Key": "PatchGroup",
                    "Value": "PilotAutoReboot"
                },
                {
                    "Key": "Schedule",
                    "Value": "Irvine-Business-Hours:M-F from 8:00AM to 6:00PM (GMT-7/8)"
                },
                {
                    "Key": "Validated",
                    "Value": "No"
                }
            ]
        }
    ]
)