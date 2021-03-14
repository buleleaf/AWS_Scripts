#!/usr/binv/env python3
import functools
import os
import csv
import boto3


@functools.lru_cache()
def boto3_client(resource, region=os.environ['AWS_DEFAULT_REGION']):
    """Create Boto3 Client from resource and region."""
    return boto3.client(resource, region)


def list_to_dict(obj, key='Key', value='Value'):
    return {e[key]: e[value] for e in obj}


def describe_instances(**kwargs):
    for page in boto3_client('ec2').get_paginator('describe_instances').paginate(**kwargs):
        for reservation in page['Reservations']:
            for instance in reservation['Instances']:
                instance['Tags'] = list_to_dict(instance['Tags'])
                yield instance

def get_prod_instances(**kwargs):
    for instances in describe_instances(Filters=[{'Name': 'tag:Environment', 'Values':  'Production'}]):
        yield instances


def list_prod_instances(prod_instances):
    for servers in get_prod_instances():
        for reservation in servers['Reservations']:
            for instance in reservation['Instances']:
                prod_instances.append(instance)


def main():
    prod_instances = []
    list_prod_instances(prod_instances)
    print(prod_instances)



if __name__ == '__main__':
    main()