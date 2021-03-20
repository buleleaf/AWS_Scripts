import boto3

from .utils import list_to_dict


class AutoScaling:
    def __init__(self, region):
        self._client = boto3.client('autoscaling', region)

    def describe_auto_scaling_groups(self, **kwargs):
        for page in self._client.get_paginator(
            'describe_auto_scaling_groups'
        ).paginate(**kwargs):
            for asg in page['AutoScalingGroups']:
                asg['Tags'] = list_to_dict(asg['Tags'])
                yield asg

class SNS:
    def __init__(self, region):
        self._client = boto3.client('sns', region):

    def publish(self, **kwargs):
        return self._client.publish(**kwargs)
