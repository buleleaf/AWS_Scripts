#!/usr/binv/env python3
import functools
import os
import csv
import boto3


def ssm_describe_instance_information(client):
    instances = []
    paginator = boto3.client('ssm').get_paginator('describe_instance_information')
    page = paginator.paginate()
    for response in page:
        for instanceinfo in response['InstanceInformationList']:
            if (instanceinfo['InstanceId']):
                instances.append(instanceinfo['InstanceId'])
    return instances



def main():
    client = boto3.client('ssm', 'eu-central-1')
    ssm_describe_instance_information(client)
    instance = ssm_describe_instance_information(client)

    for i in instance:
        print(i)

if __name__ == '__main__':
    main()