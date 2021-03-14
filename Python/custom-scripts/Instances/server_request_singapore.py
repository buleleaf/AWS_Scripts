import boto3
import time
from collections import defaultdict

region = 'ap-southeast-1'
ami_id = 'ami-01247b8894d425ad8' # Windows_Server-2012-R2_RTM-English-64Bit-Base
keyname = 'aws-singapore-corpinfo-msp'
instance_type = 't3.large'

# Shared Services VPC
subnet_id = 'subnet-5c59df2a'
sg_1 = 'sg-03f0841e838641570'

# IAM ROLE

# EBS
root_drive = '/dev/sda1'
root_drive_size = 80
root_drive_type = 'gp2'

# second_drive = 'xvdd'
# second_drive_size = 500
# second_drive_type = 'gp2'

# third_drive = 'xvde'
# third_drive_size = 500
# third_drive_type = 'gp2'

ec2 = boto3.resource('ec2', region_name=region)


instance = ec2.create_instances(
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
        # {
        #     'DeviceName': second_drive,
        #     'Ebs': {
        #         'VolumeSize': second_drive_size,
        #         'VolumeType': second_drive_type,
        #         'Encrypted': True,

        #     },
        # },
        #         {
        #     'DeviceName': third_drive,
        #     'Ebs': {
        #         'VolumeSize': third_drive_size,
        #         'VolumeType': third_drive_type,
        #         'Encrypted': True,

        #     },
        # }
    ],
    KeyName=keyname,
    NetworkInterfaces=[
        {
            'AssociatePublicIpAddress': False,
            'DeviceIndex': 0,
            'SubnetId': subnet_id,
            'Groups': [
                sg_1,
                # sg_2,
                # sg_3,
            ]

        }
    ],
    TagSpecifications=[
        {
            'ResourceType': 'instance',
            'Tags': [
                {
                    "Key": "Application",
                    "Value": "Camstar MES v6 with Camstar InterOperability"
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
                    "Value": "No"
                },
                {
                    "Key": "Environment",
                    "Value": "Test"
                },
                {
                    "Key": "Name",
                    "Value": "AWSI-TSMESCIO01"
                },
                {
                    "Key": "CorpInfoMSP:TakeNightlySnapshot",
                    "Value": "No"
                },
                {
                    "Key": "FileBackup",
                    "Value": "No"
                },
                {
                    "Key": "MonitoredServices",
                    "Value": "No"
                },
                {
                    "Key":"RequestNumber",
                    "Value":"RITM0063577"
                },
                {
                    "Key": "OperationalHours",
                    "Value": "24x7"
                },
                {
                    "Key": "ReviewDate",
                    "Value": "12/4/2022"
                },
                {
                    "Key": "CostCenter",
                    "Value": "1001798953.60055608"
                },
                {
                    "Key": "ServiceLocation",
                    "Value": "APAC"
                },
                {
                    "Key": "ServiceOwner",
                    "Value": "Craig Adams"
                },
                {
                    "Key": "TechnicalOwner",
                    "Value": "David Tower"
                },
                {
                    "Key": "ContactPreference",
                    "Value": "Email"
                },
                {
                    "Key": "PatchGroup",
                    "Value": "PilotManualReboot"
                },
                {
                    "Key": "Schedule",
                    "Value": "AlwaysOn"
                },
                {
                    "Key": "Purpose",
                    "Value": "MES integration server for Singapore Test MES environment."
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
                    "Value": "Camstar MES v6 with Camstar InterOperability"
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
                    "Value": "No"
                },
                {
                    "Key": "Environment",
                    "Value": "Test"
                },
                {
                    "Key": "Name",
                    "Value": "AWSI-TSMESCIO01"
                },
                {
                    "Key": "CorpInfoMSP:TakeNightlySnapshot",
                    "Value": "No"
                },
                {
                    "Key": "FileBackup",
                    "Value": "No"
                },
                {
                    "Key": "MonitoredServices",
                    "Value": "No"
                },
                {
                    "Key":"RequestNumber",
                    "Value":"RITM0063577"
                },
                {
                    "Key": "OperationalHours",
                    "Value": "24x7"
                },
                {
                    "Key": "ReviewDate",
                    "Value": "12/4/2022"
                },
                {
                    "Key": "CostCenter",
                    "Value": "1001798953.60055608"
                },
                {
                    "Key": "ServiceLocation",
                    "Value": "APAC"
                },
                {
                    "Key": "ServiceOwner",
                    "Value": "Craig Adams"
                },
                {
                    "Key": "TechnicalOwner",
                    "Value": "David Tower"
                },
                {
                    "Key": "ContactPreference",
                    "Value": "Email"
                },
                {
                    "Key": "PatchGroup",
                    "Value": "PilotManualReboot"
                },
                {
                    "Key": "Schedule",
                    "Value": "AlwaysOn"
                },
                {
                    "Key": "Purpose",
                    "Value": "MES integration server for Singapore Test MES environment."
                },
                {
                    "Key": "Validated",
                    "Value": "No"
                }
            ]
        },
    ]
)

time.sleep(2)

instance_status = ec2.instances.filter(Filters=[{
    'Name': 'instance-state-name',
    'Values': ['pending']}])


ec2info = defaultdict()
for instance in instance_status:
    ec2info[instance.id] = {
        'Type': instance.instance_type,
        'ID': instance.id,
        'Private IP': instance.private_ip_address,
        'State': instance.state['Name'],
        }

attributes = ['Type', 'ID', 'Private IP', 'State']
for instance_id, instance in ec2info.items():
    for key in attributes:
        print("{0}: {1}".format(key, instance[key]))
    print("-------------------------")
