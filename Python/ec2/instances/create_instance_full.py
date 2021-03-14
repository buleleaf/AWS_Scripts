import random
import string
import boto3
import time
from collections import defaultdict

region = 'us-west-2'

# def passwordGenerator(stringLength=20):
#     """ Generates a random string of fixed length"""
#     password_characters = string.ascii_letters + string.digits + string.punctuation
#     return ''.join(random.choice(password_characters) for i in range(stringLength))

# print("RDS Instance has been created with a random Master Password.")
# print(f"Please give this to the customer via LastPass: {passwordGenerator(20)}")

# AMI
#ami_id = 'ami-0f2176987ee50226e' # Amazon Linux AMI
# ami_id = 'ami-082b5a644766e0e6f' # Amazon Linux 2
#ami_id = 'ami-02deb4589e0f0d95e' # Rhel 7.6 ami-02deb4589e0f0d95e
# ami_id = 'ami-065a7bcae9ede7345' # Windows Server 2016
ami_id = 'ami-0e999cbd62129e3b1' #AZ2

#keyname = 'aws-corpinfo-msp'
keyname = 'onica-test'
instance_type = 't2.small'
subnet_id = 'subnet-041aa1b3093903949'
sg_1 = 'sg-063d908e08a4a0f46'
sg_2 = 'sg-0eb7c85ab495eb823'
# sg_3 = 'sg-c00961a6' #SG-SS-MGMT-RDPSSH-IN


# EBS
root_drive = '/dev/sda1'
root_drive_size = 80
root_drive_type = 'gp2'

# second_drive = 'xvdd'
# second_drive_size = 100
# second_drive_type = 'gp2'

ec2 = boto3.resource('ec2', region_name=region)


instance = ec2.create_instances(
    ImageId=ami_id,
    MinCount=1,
    MaxCount=1,
    InstanceType=instance_type,
    # BlockDeviceMappings=[
    #     {
    #         'DeviceName': root_drive,
    #         'Ebs': {
    #             'VolumeSize': root_drive_size,
    #             'VolumeType': root_drive_type,
    #             'Encrypted': True,

    #         },
    #     },
        # {
        #     'DeviceName': second_drive,
        #     'Ebs': {
        #         'VolumeSize': second_drive_size,
        #         'VolumeType': second_drive_type,
        #         'Encrypted': True,

        #     },
        #},
    # ],
    KeyName=keyname,
    # SecurityGroupIds=[

    # ],
    NetworkInterfaces=[
        {
            'AssociatePublicIpAddress': False,
            'DeviceIndex': 0,
            'SubnetId': subnet_id,
            'Groups': [
                sg_1,
                sg_2,
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
                    "Value": "Test"
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
                    "Value": 'ONICA-TEST-LINUX'
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
                    "Value":"Test"
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
                    "Value": "n/a"
                },
                {
                    "Key": "ServiceLocation",
                    "Value": "Irvine"
                },
                {
                    "Key": "ServiceOwner",
                    "Value": "n/a"
                },
                {
                    "Key": "TechnicalOwner",
                    "Value": "david.mansfield@rackspace.com"
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
                    "Value": "Test"
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
                    "Value": 'ONICA-TEST-LINUX'
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
                    "Value":"Test"
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
                    "Value": "n/a"
                },
                {
                    "Key": "ServiceLocation",
                    "Value": "Irvine"
                },
                {
                    "Key": "ServiceOwner",
                    "Value": "n/a"
                },
                {
                    "Key": "TechnicalOwner",
                    "Value": "david.mansfield@rackspace.com"
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
        }
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