#!/usr/bin/env python3
import boto3
import os
if not os.environ.get('AWS_DEFAULT_REGION'):
    os.environ['AWS_DEFAULT_REGION'] = 'us-west-2'
# Create CloudWatch client
cloudwatch = boto3.client('cloudwatch')

client = boto3.client('elbv2')
target_groups = []
for lb in client.describe_load_balancers()['LoadBalancers']:
    if not lb['LoadBalancerName'].startswith('dr-genius-drg'):
        continue
    if 'prod' in lb['LoadBalancerName']:
        continue
    print(lb['LoadBalancerName'])
    for target_group in client.describe_target_groups(LoadBalancerArn=lb['LoadBalancerArn'])['TargetGroups']:
        target_group_arn = target_group['TargetGroupArn'].split(':')
        target_groups.append(target_group_arn[5])

alarms = []

for response in cloudwatch.get_paginator('describe_alarms').paginate():
    for alarm in response['MetricAlarms']:
        dims = {d['Name']: d['Value'] for d in alarm['Dimensions']}
        if 'TargetGroup' in dims and dims['TargetGroup'] in target_groups and alarm['ActionsEnabled']:
            alarms.append(alarm['AlarmName'])

print('Found alarms:')
print(alarms)
# quit()
# Disable alarm
cloudwatch.disable_alarm_actions(
    AlarmNames=alarms,
)
