import random
import string
import boto3
import time
from collections import defaultdict

client = boto3.client('ec2', region_name='us-west-2')

# paginator = client.get_paginator('describe_instance_status')

# responses = paginator.paginate(
responses = client.describe_instance_status(
    Filters=[
        {
            'Name': 'instance-state-name',
            'Values': [
                'running',
            ]
        },
    ],
    InstanceIds=[
        'i-02eb397ec1da7abe1',
        'i-0afc00592cfe9bacf',
        'i-0a38fb77f7ea628ba',
        'i-030c3ace035cb39bc',
        'i-47732c5f',
        'i-04721fca4b6ca4c22',
        'i-094385b3eb8bc3f72',
        'i-08333bbf229da809d',
        'i-bd5ba1e2',
        'i-0daa9d560791bdc8c',
        'i-98f41283',
        'i-0b13ec28e89ba1fdc',
        'i-def52881',
        'i-05cceebbdb856fd8c',
        'i-09f6ce9f774e9783e',
        'i-07561ef488a6f44ce',
        'i-509b8048',
        'i-0a6c85896a2e02862',
        'i-7529b4e1',
        'i-097cc769325358a6c',
        'i-09e68fca17791facf',
        'i-061213f35072b88d0',
        'i-bdf429e2',
        'i-05011815b7fecda81',
        'i-056e0dc3583fae9e4',
        'i-f606dbee',
        'i-08a45bcff5908bbd1',
        'i-00d65932893fde636',
        'i-08c4455fb37731bb3',
        'i-a394530c',
        'i-050c1790',
        'i-04b1e9d9ec359e888',
        'i-056d2000b7a09d539',
        'i-0f8af50589e6b0387',
        'i-0014c68e9a090636b',
        'i-327ebfa6',
        'i-0303ffddb485d8a33',
        'i-0ae0dd24e1ed0018b',
        'i-0ce36af1583479f61',
        'i-d159a38e',
        'i-041f2dc5a8f247140',
        'i-b6454bae'

    ],
    # PaginationConfig={
    #     'MaxItems': 200,
    #     'PageSize': 10,
    # }
)

# instance_result = set()
# for instance_statuses in responses['InstanceStatuses']:
#     for instance_id in instance_statuses['InstanceId']:
#         instance_result.add(instance_id['InstanceId'])
# print(len(instance_result))
# print(instance_result)

instance_result = set()
for instance_statuses in responses['InstanceStatuses']:
    instance_result.add(instance_statuses['InstanceId'])
print(instance_result)

# instance_result = set()
# for reservations in responses['Reservations']:
#     for instance in reservations['Instances']:
#         if (instance['InstanceId']):
#             instance_result.add(instance['InstanceId'])
# print(len(instance_result))
# print(instance_result)


# instance_result = set()
# for reservations in responses['Reservations']:
#     for instance in reservations['Instances']:
#         if (instance['InstanceId']):
#             instance_result.add(instance['InstanceId'])
# print(len(instance_result))
# print(instance)