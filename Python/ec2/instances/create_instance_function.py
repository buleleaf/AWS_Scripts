import random
import string
import boto3
import time
from collections import defaultdict




# sg_1 = 'sg-063d908e08a4a0f46'
# sg_2 = 'sg-0eb7c85ab495eb823'

def create_instance(region, ami, subnet_id, keyname):
    ec2 = boto3.resource('ec2', region_name=region)
    instance = ec2.create_instances(
        ImageId=ami,
        MinCount=1,
        MaxCount=1,
        KeyName=keyname,
        InstanceType='t2.small',
        NetworkInterfaces=[
            {
                'AssociatePublicIpAddress': True,
                'DeviceIndex': 0,
                'SubnetId': subnet_id,
                # 'Groups': [
                #     sg_1,
                #     sg_2
                # ]

            }
        ],
        TagSpecifications=[
            {
                'ResourceType': 'instance',
                'Tags': [
                    {
                        "Key": "Name",
                        "Value": "dmansfield-test"
                    }
                    # {
                    #     "Key": "Application",
                    #     "Value": "Test"
                    # },
                    # {
                    #     "Key": "ApplicationTier",
                    #     "Value": "Application"
                    # },
                    # {
                    #     "Key": "ApplicationTierLevel",
                    #     "Value": "No Tier"
                    # },
                    # {
                    #     "Key": "Managed",
                    #     "Value": "Yes"
                    # },
                    # {
                    #     "Key": "Environment",
                    #     "Value": "Test"
                    # },
                    # {
                    #     "Key": "Name",
                    #     "Value": 'ONICA-TEST-LINUX'
                    # },
                    # {
                    #     "Key": "CorpInfoMSP:TakeNightlySnapshot",
                    #     "Value": "No"
                    # },
                    # {
                    #     "Key": "FileBackup",
                    #     "Value": "No"
                    # },
                    # {
                    #     "Key": "MonitoredServices",
                    #     "Value": "No"
                    # },
                    # {
                    #     "Key":"RequestNumber",
                    #     "Value":"Test"
                    # },
                    # {
                    #     "Key": "OperationalHours",
                    #     "Value": "24x7"
                    # },
                    # {
                    #     "Key": "ReviewDate",
                    #     "Value": "6/25/2019"
                    # },
                    # {
                    #     "Key": "CostCenter",
                    #     "Value": "n/a"
                    # },
                    # {
                    #     "Key": "ServiceLocation",
                    #     "Value": "Irvine"
                    # },
                    # {
                    #     "Key": "ServiceOwner",
                    #     "Value": "n/a"
                    # },
                    # {
                    #     "Key": "TechnicalOwner",
                    #     "Value": "david.mansfield@rackspace.com"
                    # },
                    # {
                    #     "Key": "ContactPreference",
                    #     "Value": "Email"
                    # },
                    # {
                    #     "Key": "PatchGroup",
                    #     "Value": "PilotAutoReboot"
                    # },
                    # {
                    #     "Key": "Schedule",
                    #     "Value": "24x7"
                    # },
                    # {
                    #     "Key": "Purpose",
                    #     "Value": "N/A"
                    # },
                    # {
                    #     "Key": "Validated",
                    #     "Value": "No"
                    # }
                ]
            },
            {
                'ResourceType': 'volume',
                'Tags': [
                    {
                        "Key": "Name",
                        "Value": "dmansfield-test"
                    }
                    # {
                    #     "Key": "Application",
                    #     "Value": "Test"
                    # },
                    # {
                    #     "Key": "ApplicationTier",
                    #     "Value": "Application"
                    # },
                    # {
                    #     "Key": "ApplicationTierLevel",
                    #     "Value": "No Tier"
                    # },
                    # {
                    #     "Key": "Managed",
                    #     "Value": "Yes"
                    # },
                    # {
                    #     "Key": "Environment",
                    #     "Value": "Test"
                    # },
                    # {
                    #     "Key": "Name",
                    #     "Value": 'ONICA-TEST-LINUX'
                    # },
                    # {
                    #     "Key": "CorpInfoMSP:TakeNightlySnapshot",
                    #     "Value": "No"
                    # },
                    # {
                    #     "Key": "FileBackup",
                    #     "Value": "No"
                    # },
                    # {
                    #     "Key": "MonitoredServices",
                    #     "Value": "No"
                    # },
                    # {
                    #     "Key":"RequestNumber",
                    #     "Value":"Test"
                    # },
                    # {
                    #     "Key": "OperationalHours",
                    #     "Value": "24x7"
                    # },
                    # {
                    #     "Key": "ReviewDate",
                    #     "Value": "6/25/2019"
                    # },
                    # {
                    #     "Key": "CostCenter",
                    #     "Value": "n/a"
                    # },
                    # {
                    #     "Key": "ServiceLocation",
                    #     "Value": "Irvine"
                    # },
                    # {
                    #     "Key": "ServiceOwner",
                    #     "Value": "n/a"
                    # },
                    # {
                    #     "Key": "TechnicalOwner",
                    #     "Value": "david.mansfield@rackspace.com"
                    # },
                    # {
                    #     "Key": "ContactPreference",
                    #     "Value": "Email"
                    # },
                    # {
                    #     "Key": "PatchGroup",
                    #     "Value": "PilotAutoReboot"
                    # },
                    # {
                    #     "Key": "Schedule",
                    #     "Value": "24x7"
                    # },
                    # {
                    #     "Key": "Purpose",
                    #     "Value": "N/A"
                    # },
                    # {
                    #     "Key": "Validated",
                    #     "Value": "No"
                    # }
                ]
            }
        ]
    )
    return(instance)

def main():
    region = 'us-west-2'
    ami = 'ami-077475371a476c548' # Windows 2019 Base
    subnet_id = 'subnet-0580e4b1ffde93c4e'
    keyname = 'dmansfield'

    create_instance(region, ami, subnet_id, keyname)




if __name__ == '__main__':
    main()