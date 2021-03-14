#!/usr/bin/env python3
"""See what instances have CW agent installed and working correctly.

No CW Agent (and instances which may have the agent but no metrics)
Instances with a possibly misconfigured agent
Memory Metrics script
CW Agent
"""
import csv
import sys
import argparse
import os
import json
import logging
import boto3

from botocore.exceptions import ClientError

FORMAT = '%(asctime)-15s %(levelname)s %(module)s.%(funcName)s %(message)s'
DATEFMT = "%Y-%m-%d %H:%M:%S"
logging.basicConfig(level=logging.INFO, format=FORMAT, datefmt=DATEFMT)


METRICS = {
    'Windows/System': {
        'MemoryUsed': 'InstanceId'
    }
}


def list_to_dict(data):
    return {o['Key']: o['Value'] for o in data}


def convert_tags_ec2_instance(instance):
    instance.update(**list_to_dict(instance.get('Tags', [])))
    return instance


def describe_instances(client):
    paginator = client.get_paginator('describe_instances')
    for page in paginator.paginate(
        Filters=[{
            'Name': 'instance-state-name',
            'Values': ['running']}]):
        for reservation in page['Reservations']:
            for instance in reservation['Instances']:
                yield convert_tags_ec2_instance(instance)


def process_instance(instance, cw_client):
    win_metrics = cw_client.list_metrics(
        Namespace='System/Windows',
        Dimensions=[{
            "Name": "InstanceId",
            "Value": instance['InstanceId']
        }])

    linux_metrics = cw_client.list_metrics(
        Namespace='System/Linux',
        Dimensions=[{
            "Name": "InstanceId",
            "Value": instance['InstanceId']
        }])

    if len(win_metrics["Metrics"]) > 0:
        if 'LogicalDisk % Free Space' in [m['MetricName'] for m in win_metrics["Metrics"]]:
            metrics = "CW Agent (Win)"
        else:
            metrics = "Mem Metrics (Win)"
    elif len(linux_metrics["Metrics"]) > 0:
        if 'disk_used_percent' in [m['MetricName'] for m in linux_metrics["Metrics"]]:
            metrics = "CW Agent (Linux)"
        else:
            metrics = "Mem Metrics (Linux)"
    else:
        logging.warning('%s has no cw agent', instance['InstanceId'])
        logging.warning('Windows Metrics: %s\nLinux Metrics: %s', win_metrics["Metrics"], linux_metrics["Metrics"])
        metrics = "Missing"
    logging.debug('Detected %s for %s(%s)', metrics, instance.get('Name', 'undefined'), instance['InstanceId'])
    return metrics


def main():
    if sys.version_info[0] < 3:
        raise Exception("Must be using Python 3")
    region = os.getenv('AWS_REGION', os.getenv('AWS_DEFAULT_REGION', 'us-west-2'))
    ec2_client = boto3.client('ec2', region)
    cw_client = boto3.client('cloudwatch', region)

    data = []
    undefined_count = 1
    for instance in describe_instances(ec2_client):
        metrics = process_instance(instance, cw_client)
        if instance.get('Name'):
            data.append([instance.get('Name'), instance.get('InstanceId'), metrics])
        else:
            data.append(['undefined' + str(undefined_count), instance.get('InstanceId'), metrics])
            undefined_count += 1
    with open('report.json', 'w') as outfile:
        outfile.write(json.dumps(data, indent=4))
    with open('report.csv', 'w') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(['InstanceName', 'InstanceId', 'Status'])
        for row in data:
            writer.writerow(row)


if __name__ == '__main__':
    main()
