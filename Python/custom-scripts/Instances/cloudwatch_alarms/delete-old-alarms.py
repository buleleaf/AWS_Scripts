#!/usr/bin/env python3
"""Script to find all alarms which do not conform to the current naming scheme and delete them."""
import os
import boto3
from botocore.exceptions import ClientError
import logging

FORMAT = '%(asctime)-15s %(levelname)s %(module)s.%(funcName)s %(message)s'
DATEFMT = "%Y-%m-%d %H:%M:%S"
logging.basicConfig(level=logging.INFO, format=FORMAT, datefmt=DATEFMT)
REGION = os.getenv('AWS_REGION', 'us-west-2')
ALARM_SHCEME = '{InstanceId}-{InstanceName}-{MetricName}'


def convert_list_to_dict(obj, key='Key', value='Value'):
    return {e[key]: e[value] for e in obj}


def describe_instances(client, instanceids):
    instances = []
    for instanceid in instanceids:
        try:
            response = client.describe_instances(InstanceIds=[instanceid])
        except ClientError as error:
            logging.info('%s does not exist', instanceid)
            continue
        else:
            for reservations in response['Reservations']:
                for instance in reservations['Instances']:
                    instance['Tags'] = convert_list_to_dict(instance['Tags'])
                    instances.append(instance)
    return instances

def get_instance_map(instances):
    instance_map = {}
    for instance in instances:
        instance_map[instance['InstanceId']] = instance['Tags'].get('Name', None)
    return instance_map

class GetAlarms():
    def __init__(self, client):
        self.client = client
        self.namespaces = set()
        self.metricnames = set()
        self.alarms = {}
        self.alarm_count = 0

    def describe_alarms(self, **kwargs):
        paginator = self.client.get_paginator('describe_alarms')
        response_iterator = paginator.paginate(**kwargs)
        for page in response_iterator:
            for alarm in page['MetricAlarms']:
                yield alarm

    def get_alarms(self):
        for alarm in self.describe_alarms():
            dimensions = convert_list_to_dict(alarm['Dimensions'], 'Name', 'Value')
            self.namespaces.add(alarm['Namespace'])
            self.metricnames.add(alarm['MetricName'])
            if 'InstanceId' not in dimensions:
                continue
            self.alarm_count += 1
            if dimensions['InstanceId'] not in self.alarms:
                self.alarms[dimensions['InstanceId']] = {}
            if alarm['Namespace'] not in self.alarms[dimensions['InstanceId']]:
                self.alarms[dimensions['InstanceId']][alarm['Namespace']] = {}
            metricname = alarm['MetricName']
            if metricname == 'LogicalDisk % Free Space' and 'instance' in dimensions:
                metricname = metricname + dimensions['instance']
            if metricname not in self.alarms[dimensions['InstanceId']][alarm['Namespace']]:
                self.alarms[dimensions['InstanceId']][alarm['Namespace']][metricname] = []
            self.alarms[dimensions['InstanceId']][alarm['Namespace']][metricname].append(alarm)


def main():
    client = boto3.client('cloudwatch', REGION)
    get_alarms = GetAlarms(client)
    get_alarms.get_alarms()
    instance_map = get_instance_map(
        describe_instances(
            boto3.client('ec2', REGION),
            list(get_alarms.alarms.keys())))
    logging.info('Unique Namespaces: %s', ', '.join(get_alarms.namespaces))
    logging.info('Unique MetricNames: %s', ', '.join(get_alarms.metricnames))
    logging.info('Unique Instances: %s', len(get_alarms.alarms.keys()))
    logging.debug('Unique Instances: %s', ', '.join(get_alarms.alarms.keys()))
    logging.info('Found %s total alarms', get_alarms.alarm_count)
    multiple_alarm_count = 0
    bad_alarms = []
    for instanceid in get_alarms.alarms:
        for namespace in get_alarms.alarms[instanceid]:
            for metricname in get_alarms.alarms[instanceid][namespace]:
                for alarm in get_alarms.alarms[instanceid][namespace][metricname]:
                    if instanceid not in instance_map or not alarm['AlarmName'].startswith('{}-{}'.format(instanceid, instance_map[instanceid])):
                        bad_alarms.append(alarm)
                # if len(get_alarms.alarms[instanceid][namespace][metricname]) > 1:
                #     multiple_alarm_count += 1
                #     logging.warning('Found multiple entries for %s for %s: %s\n'
                #                     'Alarms: %s', instanceid, namespace,
                #                     metricname, ', '.join(
                #                         [a['AlarmName']
                #                          for a in get_alarms.alarms[instanceid][namespace][metricname]]))
    logging.info('Found %s alarms with duplicate entries', multiple_alarm_count)
    logging.info('Found %s total alarms which are malformed\nAlarms:\n%s',
                 len(bad_alarms),
                 ', '.join([
                     a['AlarmName']
                     for a in bad_alarms
                 ]))


if __name__ == '__main__':
    main()