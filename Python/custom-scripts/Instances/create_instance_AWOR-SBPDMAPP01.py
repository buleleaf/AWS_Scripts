import boto3
import time
from collections import defaultdict

region = 'us-west-2'
#ami_id = 'ami-02deb4589e0f0d95e' # Rhel 7.6 ami-02deb4589e0f0d95e
ami_id = 'ami-0d705356e2616369c' # Windows Server 2016
keyname = 'aws-corpinfo-msp'
instance_type = 't2.medium'
subnet_id = 'subnet-594fb32f' # Shared Services VPC Protected A
sg_1 = 'sg-85375fe3' # SG-SS-MGMT-ALLTRAFFIC-OUT
sg_2 = 'sg-ed08608b' #SG-SS-MGMT-CORESERVICES
sg_3 = 'sg-c00961a6' #SG-SS-MGMT-RDPSSH-IN


# EBS
root_drive = '/dev/sda1'
root_drive_size = 80
root_drive_type = 'gp2'

second_drive = 'xvdd'
second_drive_size = 100
second_drive_type = 'gp2'

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
    SecurityGroupIds=[

    ],
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
                    "Value": "Windchill"
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
                    "Value": "Development"
                },
                {
                    "Key": "Name",
                    "Value": "AWOR-SBPDMAPP01"
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
                    "Value":"RITM0032252"
                },
                {
                    "Key": "OperationalHours",
                    "Value": "24x7"
                },
                {
                    "Key": "ReviewDate",
                    "Value": "6/25/2019"
                },
                {
                    "Key": "CostCenter",
                    "Value": "1001596013"
                },
                {
                    "Key": "ServiceLocation",
                    "Value": "Irvine"
                },
                {
                    "Key": "ServiceOwner",
                    "Value": "Amir Memaran"
                },
                {
                    "Key": "TechnicalOwner",
                    "Value": "Alek Slavuk"
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
                    "Value": "24x7"
                },
                {
                    "Key": "Purpose",
                    "Value": "N/A"
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
                    "Value": "Windchill"
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
                    "Value": "Development"
                },
                {
                    "Key": "Name",
                    "Value": "AWOR-SBPDMAPP01"
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
                    "Value": "RITM0032252"
                },
                {
                    "Key": "OperationalHours",
                    "Value": "24x7"
                },
                {
                    "Key": "ReviewDate",
                    "Value": "6/25/2019"
                },
                {
                    "Key": "CostCenter",
                    "Value": "1001596013"
                },
                {
                    "Key": "ServiceLocation",
                    "Value": "Irvine"
                },
                {
                    "Key": "ServiceOwner",
                    "Value": "Amir Memaran"
                },
                {
                    "Key": "TechnicalOwner",
                    "Value": "Alek Slavuk"
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
                    "Value": "24x7"
                },
                {
                    "Key": "Purpose",
                    "Value": "Windchill 11.2 Sandbox System"
                },
                {
                    "Key": "Validated",
                    "Value": "No"
                }
            ]
        }
    ]
)

time.sleep(5)

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
