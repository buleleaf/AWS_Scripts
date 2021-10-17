#!/usr/bin/python

import random
import string
import boto3
import time
from collections import defaultdict

# sg_1 = 'sg-063d908e08a4a0f46'
# sg_2 = 'sg-0eb7c85ab495eb823'

# user_data ='''#!/bin/bash
# sudo yum update -y  &&
# pip3 install runway &&

#  # GitLab Runner DL and install 
# sudo curl -L https://packages.gitlab.com/install/repositories/runner/gitlab-runner/script.rpm.sh | sudo bash && \\
# sudo curl -L --output /usr/local/bin/gitlab-runner https://gitlab-runner-downloads.s3.amazonaws.com/latest/binaries/gitlab-runner-linux-amd64 && \\
# export GITLAB_RUNNER_DISABLE_SKEL=true; sudo -E yum install gitlab-runner -y

# sleep 30 &

#  # Terraform DL and install 

# TERRAFORM_VER=`curl -s https://api.github.com/repos/hashicorp/terraform/releases/latest |  grep tag_name | cut -d: -f2 | tr -d \"\,\v | awk '{$1=$1};1'`
# sudo wget https://releases.hashicorp.com/terraform/${TERRAFORM_VER}/terraform_${TERRAFORM_VER}_linux_amd64.zip &&
# sudo unzip terraform_${TERRAFORM_VER}_linux_amd64.zip &&
# sudo mv terraform /usr/local/bin/'''

def create_instance(region, ami, subnet_id, keyname):
    ec2 = boto3.resource('ec2', region_name=region)
    instance = ec2.create_instances(
        ImageId=ami,
        MinCount=1,
        MaxCount=1,
        KeyName=keyname,
        InstanceType='t2.micro',
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
        # UserData = user_data,
        TagSpecifications=[
            {
                'ResourceType': 'instance',
                'Tags': [
                    {
                        "Key": "Name",
                        "Value": "GitLab Runner"
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
    region = 'us-east-2'
    ami = 'ami-074cce78125f09d61' # AL2
    subnet_id = 'subnet-05ba474a74110b5d9'
    keyname = 'dmansfield-lab'

    create_instance(region, ami, subnet_id, keyname)




if __name__ == '__main__':
    main()