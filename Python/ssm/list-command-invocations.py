#!/usr/binv/env python3
import functools
import os
import csv
import boto3


paginator = boto3.client('ssm').get_paginator('list_command_invocations')
page = paginator.paginate(
    Filters=[
        {
            'key': 'Status',
            'value': 'Failed',
        },
        {
            'key': 'InvokedAfter',
            'value': '2020-10-24T12:42:00Z'
        },
        {
            'key': 'InvokedBefore',
            'value': '2020-10-25T22:00:00Z'
        },
    ],
)


# instances = []
# for response in page:
#     for command in response['CommandInvocations']:
#         print(command['InstanceId'])

for response in page:
    for command in response['CommandInvocations']:
        print(command['InstanceId'])

    # for response in page:
    #     for instanceinfo in response['InstanceInformationList']:
    #         if (instanceinfo['InstanceId']):
    #             instances.append(instanceinfo['InstanceId'])
    # return instances