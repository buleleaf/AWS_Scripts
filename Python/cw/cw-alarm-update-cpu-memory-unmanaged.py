#!/usr/bin/env python3
"""Update all existing memory and CPU alarms to be sent to the unmanaged topic"""
# Find all CPU/Memory Alarms
# Update actions to unmanaged
import argparse
import functools
import logging
import os
import sys
from multiprocessing.dummy import Pool, current_process

import boto3

FORMAT = '%(asctime)-15s %(levelname)s %(module)s.%(funcName)s %(message)s'
DATEFMT = "%Y-%m-%d %H:%M:%S"
logging.basicConfig(level=logging.INFO, format=FORMAT, datefmt=DATEFMT)
os.environ['AWS_DEFAULT_REGION'] = 'us-east-1'


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--region', default='us-west-2')
    parser.add_argument('--dry-run', action='store_true')
    return vars(parser.parse_args())


def boto3_client(resource, region):
    return boto3.client(resource, region)


def munge_alarm_actions(alarm, old_action, new_action):
    """Update alarm action which has old action and replace with new_action."""
    changed_actions = False
    for key in ('OKActions', 'AlarmActions', 'InsufficientDataActions'):
        new_actions = replace_actions(
            alarm.get(key, []), old_action, new_action
        )
        if new_actions != alarm[key]:
            alarm[key] = new_actions
            changed_actions = True
    return alarm, changed_actions


def update_cw_alarm_actions(client, old_action, new_action, alarm):
    new_alarm, changed_actions = munge_alarm_actions(
        alarm, old_action, new_action
    )
    if changed_actions:
        logging.debug('Alarm: %s', new_alarm)
        update_alarm(client, cleanup_alarm(client, new_alarm))
        logging.info('Updated Actions for %s', alarm['AlarmName'])


def update_alarm(client, alarm):
    """Update alarm."""
    return client.put_metric_alarm(**alarm)


def operation_model_kwargs(client, model_name):
    """Return the arguments we can provide to a boto3 function for the specified client."""
    return client._service_model.operation_model(
        model_name
    ).input_shape.members.keys()


def method_to_operation_model(client, method):
    """Return the Operation Model for given client and method."""
    return client._PY_TO_OP_NAME[method]


def cleanup_alarm(client, alarm, func_name='put_metric_alarm'):
    """Remove invalid arguments from specified alarm."""
    return {
        key: alarm[key]
        for key in operation_model_kwargs(
            client, method_to_operation_model(client, func_name)
        )
        if key in alarm
    }


def replace_actions(actions, old_action, new_action):
    return list({new_action if old_action else action for action in actions})


def get_all_alarms(client):
    """Gets all alarms in a region."""
    for page in client.get_paginator('describe_alarms').paginate():
        for metric_alarm in page['MetricAlarms']:
            yield metric_alarm


def allowed_metric_names():
    return ('CPUUtilization', 'MemoryUtilization')


def get_specific_metric_alarms(alarms, metricnames):
    for alarm in alarms:
        if alarm['MetricName'] in metricnames:
            yield alarm


@functools.lru_cache
def list_topics(client):
    return [
        topic
        for page in client.get_paginator('list_topics').paginate()
        for topic in page['Topics']
    ]


def sns_topic_arn_from_name(client, topic_name):
    for topic in list_topics(client):
        if topic_name in topic['TopicArn']:
            logging.info('Found %s for %s', topic['TopicArn'], topic_name)
            return topic['TopicArn']


def alarm_has_action_topic(topic_arn, alarm):
    results = []
    for key in ('OKActions', 'AlarmActions', 'InsufficientDataActions'):
        resp = False
        if topic_arn in alarm[key]:
            resp = True
        results.append(resp)
    return any(results)
    # any(
    #     [
    #         True if topic_arn in alarm[key] else False
    #         for key in ('OKActions', 'AlarmActions', 'InsufficientDataActions')
    #     ]
    # )


def main(args=parse_args()):
    # import code;code.interact(local={**globals(), **locals()})
    client = boto3_client('cloudwatch', args['region'])
    sns = boto3_client('sns', args['region'])
    update_cw_alarm_actions_high_to_unmanaged = functools.partial(
        update_cw_alarm_actions,
        client,
        sns_topic_arn_from_name(sns, 'edwards-pagerduty-high-topic'),
        sns_topic_arn_from_name(sns, 'Edwards-Unmanaged-Notifications'),
    )

    # Alarms which are for CPUUtlization or MemoryUtilization.
    alarm_has_low_topic = functools.partial(
        alarm_has_action_topic,
        sns_topic_arn_from_name(sns, 'edwards-pagerduty-low-topic'),
    )
    alarms = filter(
        alarm_has_low_topic,
        get_specific_metric_alarms(
            get_all_alarms(client), allowed_metric_names()
        ),
    )

    # import code;code.interact(local={**globals(), **locals()})
    # alarms = [a for a in alarms]
    if args['dry_run']:
        for alarm in alarms:
            print(alarm['AlarmName'])
    else:
        for alarm in alarms:
            update_cw_alarm_actions_high_to_unmanaged(alarm)


if __name__ == '__main__':
    main()
