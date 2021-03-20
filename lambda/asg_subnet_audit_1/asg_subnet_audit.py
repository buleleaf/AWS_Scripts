import os

import boto3

from .formatter import FormatReport
from .sender import SendReport, sender_sns, sender_stdout


def parse_args():
    return {'region': 'us-west-2'}


def list_to_dict(obj, key='Key', value='Value'):
    return {o[key]: o[value] for o in obj}


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


def has_stateless_ha_tag(asg):
    return 'StatelessHa' in asg['Tags']
    # return asg['Tags'].get('StatelessHa', 'no').lower() == 'yes'


def not_enough_subnets(asg):
    return len(asg['VPCZoneIdentifier'].split(',')) < 2


def enough_subnets(asg):
    return len(asg['VPCZoneIdentifier'].split(',')) >= 2


def asg_name(asg):
    return asg['AutoScalingGroupName']


def main(event, context, sender=sender_stdout):
    autoscaling_groups = list(
        filter(
            has_stateless_ha_tag,
            AutoScaling(
                os.environ['AWS_DEFAULT_REGION']
            ).describe_auto_scaling_groups(),
        )
    )

    report = {
        'Sufficient Subnets': map(
            asg_name, filter(not_enough_subnets, autoscaling_groups)
        ),
        'Insufficient Subnets': map(
            asg_name, filter(enough_subnets, autoscaling_groups)
        ),
    }
    SendReport(sender).send(FormatReport(report).format())


if __name__ == '__main__':
    main()
