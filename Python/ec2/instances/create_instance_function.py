#!/usr/bin/python

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
                ]
            },
            {
                'ResourceType': 'volume',
                'Tags': [
                    {
                        "Key": "Name",
                        "Value": "dmansfield-test"
                    }
                ]
            }
        ]
    )
    return(instance)

def main():
    region = 'us-east-1'
    ami = 'ami-0d5eff06f840b45e9' # AL2
    subnet_id = 'subnet-0a0190770c49480f8'
    keyname = 'dmansfield'

    create_instance(region, ami, subnet_id, keyname)




if __name__ == '__main__':
    main()