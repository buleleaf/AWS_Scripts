#!/usr/bin/env python3
import functools
import os
import csv
import boto3
import pprint
os.environ['AWS_DEFAULT_REGION'] = 'us-west-2'

@functools.lru_cache()
def boto3_client(resource, region=os.environ['AWS_DEFAULT_REGION']):
    """Create Boto3 Client from resource and region."""
    return boto3.client(resource, region)

def describe_asg(**kwargs):
    for page in boto3_client('autoscaling').get_paginator(
        'describe_auto_scaling_groups').paginate(**kwargs):
        for autoscalinggroup in page['AutoScalingGroups']:
            yield autoscalinggroup
    #         if (autoscalinggroup['AutoScalingGroupName']):
    #             asg_name.append(autoscalinggroup['AutoScalingGroupName'])
    # return asg_name

def describe_asg_name():
    asg_output = describe_asg()
    for asg in asg_output:
        return (asg['AutoScalingGroupName'])

# def describe_asg_subnets(**kwargs):
#     subnets = []
#     paginator = boto3.client('autoscaling').get_paginator('describe_auto_scaling_groups')
#     page = paginator.paginate(**kwargs)
#     print(paginator)
    # return page['AutoScalingGroups'][0]

    # for response in page:
    #     # pprint.pprint(response)
    #     for subnetcount in response['AutoScalingGroups']:
    #         if len(subnetcount['VPCZoneIdentifier']) <= 1:
    #             print(response['AutoScalingGroups'][0])
def main():

    # asg_output = describe_asg()
    asg_name = describe_asg_name()

    # for asg in asg_output:
    #     print(asg['AutoScalingGroupName'])

    # for asg in asg_name:
    print(asg_name)


if __name__ == '__main__':
    main()