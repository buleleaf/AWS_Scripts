#!/usr/bin/env python3
import functools
import os
import boto3

os.environ['AWS_DEFAULT_REGION'] = 'us-east-1'
new_topic = 'arn:aws:sns:us-east-1:555747502387:status-check-failed'

@functools.lru_cache
def boto3_client(resource, region=os.environ['AWS_DEFAULT_REGION']):
    """Create Boto3 Client from resource and region."""
    return boto3.client(resource, region)

def describe_instances():
    for page in (
        boto3_client('ec2').get_paginator('describe_instances').paginate()
    ):
        for reservation in page['Reservations']:
            for instance in reservation['Instances']:
                yield instance


def list_to_dict(obj, key='Key', value='Value'):
    return {e[key]: e[value] for e in obj}


def describe_alarms():
    for page in (
        boto3_client('cloudwatch').get_paginator('describe_alarms').paginate()
    ):
        for metric_alarm in page['MetricAlarms']:
            yield metric_alarm


def operation_model_kwargs(client, model_name):
    """Return the arguments we can provide to a boto3 function for the specified client."""
    return client._service_model.operation_model(
        model_name
    ).input_shape.members.keys()


def method_to_operation_model(client, method):
    """Return the Operation Model for given client and method."""
    return client._PY_TO_OP_NAME[method]


def cleanup_alarm(alarm, func_name='put_metric_alarm', client=boto3_client('cloudwatch')):
    """Remove invalid arguments from specified alarm."""
    return {
        key: alarm[key]
        for key in operation_model_kwargs(
            client, method_to_operation_model(client, func_name)
        )
        if key in alarm
    }

def process_alarm(alarm):
    # Update actions to add new topic and dedupe.
    for key in ('AlarmActions', 'OKActions'):
        alarm[key].append(new_topic)
        alarm[key] = list(set(alarm[key]))
    # Cleanup alarm definition removing invalid keys.
    alarm = cleanup_alarm(alarm)
    boto3.client('cloudwatch').put_metric_alarm(**alarm)


def _is_prod_instance(instances_env_map, alarm):
        instance_id = list_to_dict(alarm['Dimensions'], 'Name', 'Value').get(
            'InstanceId'
        )
        return instances_env_map.get(instance_id, '').lower() in ('prod', 'production',)


def _is_status_check(alarm):
    return alarm['MetricName'] in ('StatusCheckFailed',)


def main():

    instances_env_map = {
        instance['InstanceId']: list_to_dict(instance['Tags']).get(
            'Environment'
        )
        for instance in describe_instances()
    }

    # Removing None value items and updating the dict
    filtered_instances = {k: v for k, v in instances_env_map.items() if v is not None}
    instances_env_map.clear()
    instances_env_map.update(filtered_instances)

    env_tag_values = sorted(list(set(instances_env_map.values())))
    print('\n'.join(env_tag_values))

    is_prod_instance = functools.partial(_is_prod_instance, instances_env_map)


    for alarm in describe_alarms():
        if is_prod_instance(alarm) and _is_status_check(alarm):
            process_alarm(alarm)
        print(alarm)

if __name__ == '__main__':
    main()