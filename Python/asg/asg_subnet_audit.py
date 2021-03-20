import boto3
import os
import functools
import pprint

def list_to_dict(obj, key='Key', value='Value'):
    return {o[key]: o[value] for o in obj}

class AutoScaling:
    def __init__(self, region):
        self._client = boto3.client('autoscaling', region)
    def describe_auto_scaling_groups(self, **kwargs):
        for page in self._client.get_paginator('describe_auto_scaling_groups').paginate(**kwargs):
            for asg in page['AutoScalingGroups']:
                asg['Tags'] = list_to_dict(asg['Tags'])
                yield asg


def stateless_ha(asg):
    return 'StatelessHa' in asg['Tags']


def not_enough_subnets(asg):
    return len(asg['VPCZoneIdentifier'].split(",")) < 2


def enough_subnets(asg):
    return len(asg['VPCZoneIdentifier'].split(",")) >= 2


def asg_info():
    asgs = AutoScaling(os.environ['AWS_DEFAULT_REGION']).describe_auto_scaling_groups()
    asgs = list(filter(stateless_ha, asgs))
    print('not_enough_subnets')
    for asg in filter(not_enough_subnets, asgs):
        print(asg['AutoScalingGroupName'])
    print('enough_subnets')
    for asg in filter(enough_subnets, asgs):
        print(asg['AutoScalingGroupName'])


def main():
    asgs = asg_info()


if __name__ == '__main__':
    os.environ['AWS_DEFAULT_REGION'] = 'us-west-2'
    main()