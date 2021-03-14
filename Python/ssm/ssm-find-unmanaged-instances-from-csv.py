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

def read_instance_names_from_file(filename='{}-missing-metrics.csv'.format(os.environ['AWS_DEFAULT_REGION'])):
    """Reads a csv with the list of servers that are missing metrics"""
    with open(filename, newline='') as csvfile:
        return [r for r in csv.reader(csvfile)]

def add_csv_to_set(ec2_instances):
    for instances in read_instance_names_from_file():
        for i in instances:
            ec2_instances.add(i)
    return instances

def ssm_describe_instance_information(ssm_instances):
    paginator = boto3.client('ssm').get_paginator('describe_instance_information')
    page = paginator.paginate()
    for response in page:
        for instanceinfo in response['InstanceInformationList']:
            if (instanceinfo['InstanceId']):
                ssm_instances.add(instanceinfo['InstanceId'])
    return ssm_instances


def main():
    ec2_instances = set()
    ssm_instances = set()
    add_csv_to_set(ec2_instances)
    ssm_describe_instance_information(ssm_instances)
    ssm_unmanaged = ec2_instances.difference(ssm_instances)
    ssm_managed = ec2_instances.intersection(ssm_instances)


    filename = '{}-ssm-unmanaged.csv'.format(os.environ['AWS_DEFAULT_REGION'])


    # Write the list of ssm unmanaged servers to csvfile
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(ssm_unmanaged)

    # Runs send command to list of managed instances and configures Cloudwatch
    for managed in ssm_managed:
        boto3_client('ssm').send_command(
            InstanceIds=[managed],
            DocumentName='CloudWatchAgentInstallAndConfigure'
        )

if __name__ == '__main__':
    main()