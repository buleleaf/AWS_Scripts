#!/usr/binv/env python3
import functools
import os
import csv
import boto3

# This only find the instace ID's and is not complete


@functools.lru_cache()
def boto3_client(resource, region=os.environ['AWS_DEFAULT_REGION']):
    """Create Boto3 Client from resource and region."""
    return boto3.client(resource, region)

def ssm_describe_instance_information(**kwargs):
    for page in boto3_client('ssm').get_paginator('describe_instance_information').paginate(**kwargs):
        for instanceinfo in page['InstanceInformationList']:
            for instance in instanceinfo['InstanceId']:
                return instance



def main():

    instance = ssm_describe_instance_information()

    for i in instance:
        print(i)

if __name__ == '__main__':
    main()