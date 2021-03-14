#!/usr/binv/env python3
import functools
import os
import csv
import boto3
os.environ['AWS_DEFAULT_REGION'] = 'us-west-2'

@functools.lru_cache
def boto3_client(resource):
    """Create Boto3 Client."""
    return boto3.client(resource)

def list_to_dict(obj, key='Key', value='Value'):
    return {e[key]: e[value] for e in obj}

def describe_instances(**kwargs):
    for page in boto3_client('ec2').get_paginator('describe_instances').paginate(**kwargs):
        for reservation in page['Reservations']:
            for instance in reservation['Instances']:
                instance['Tags'] = list_to_dict(instance['Tags'])
                yield instance

def instance_name_to_id(instance_names):
    return describe_instances(Filters=[{'Name': 'tag:Name', 'Values':  instance_names}])

def read_instance_names_from_file(filename='instances-missing-metrics.csv'):
    with open('names.csv', newline='') as csvfile:
        return [r for r in csv.DictReader(csvfile)]

def region_instance_names(data, region='Oregon', key='Instance Name'):
    for row in data:
        if row['Region'] == region:
            yield row[key]

def send_command(doc_name, targets):
    return boto3_client('ssm').send_command(
        Targets=targets,
        DocumentName=doc_name,
    )

def main():
    doc_name = 'edwards-cloud-watch-agent-SsmDocument-19MEJ6QY1421Y'
    import code;code.interact(local={**globals(),**locals()})
    send_command(doc_name, list(region_instance_names(read_instance_names_from_file())))
    breakpoint()


if __name__ == '__main__':
    main()
