#!/usr/binv/env python3
import functools
import os
import csv
import boto3

os.environ['AWS_DEFAULT_REGION'] = 'us-west-2'

@functools.lru_cache()
def boto3_client(resource):
    """Create Boto3 Client."""
    return boto3.client(resource)

def list_to_dict(obj, key='Key', value='Value'):
    return {e[key]: e[value] for e in obj}

# def describe_instances(**kwargs):
for page in boto3_client('ec2').get_paginator('describe_instances').paginate():
    for reservation in page['Reservations']:
        for instance in reservation['Instances']:
            instance['Tags'] = list_to_dict(instance['Tags'])
            print(instance)

# def main():

#     doc_name = 'edwards-cloud-watch-agent-SsmDocument-19MEJ6QY1421Y'
#     send_command(doc_name, list(region_instance_names(read_instance_names_from_file())))
#     breakpoint()
