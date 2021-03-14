#!/usr/binv/env python3
import functools
import os
import csv
import boto3

os.environ['AWS_DEFAULT_REGION'] = 'eu-central-1'

@functools.lru_cache()
def boto3_client(resource, region=os.environ['AWS_DEFAULT_REGION']):
    """Create Boto3 Client from resource and region."""
    return boto3.client(resource, region)

def ssm_describe_instance_imformation(**kwargs):
    instances = []
    paginator = boto3.client('ssm').get_paginator('describe_instance_information')
    page = paginator.paginate(**kwargs)
    for response in page:
        for instanceinfo in response['InstanceInformationList']:
            if (instanceinfo['InstanceId']):
                instances.append(instanceinfo['InstanceId'])
    return instances

def main():
    instance = ssm_describe_instance_imformation()

    for i in instance:
        print(i)

if __name__ == '__main__':
    main()
