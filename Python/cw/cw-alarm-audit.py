#!/usr/bin/env python3
"""Script to find all alarms which do not conform to the current naming scheme and delete them."""
import os
import json
import logging
import boto3
from botocore.exceptions import ClientError

FORMAT = '%(asctime)-15s %(levelname)s %(module)s.%(funcName)s %(message)s'
DATEFMT = "%Y-%m-%d %H:%M:%S"
logging.basicConfig(level=logging.INFO, format=FORMAT, datefmt=DATEFMT)
REGION = os.getenv('AWS_REGION', 'us-west-2')
ALARM_SHCEME = '{InstanceId}-{InstanceName}-{MetricName}'
ALLOWED_SUFFIXES_4 = set(['WindowsDiskFreeSpace'])
ALLOWED_SUFFIXES_3 = set(['WindowsMemoryUtilization', 'CPUUtilization', 'LinuxMemoryUtilization', 'StatusCheckFailed'])
ALLOWED_SUFFIXES = tuple(ALLOWED_SUFFIXES_3.union(ALLOWED_SUFFIXES_4))


def convert_list_to_dict(obj, key='Key', value='Value'):
    return {e[key]: e[value] for e in obj}


def describe_all_instances(client):
    instances = []
    paginator = client.get_paginator('describe_instances')
    response = paginator.paginate()
    for page in response:
        for reservations in page['Reservations']:
            for instance in reservations['Instances']:
                instance['Tags'] = convert_list_to_dict(instance['Tags'])
                instances.append(instance)
    return instances


def describe_instances(client, instanceids):
    instances = []
    try:
        paginator = client.get_paginator('describe_instances')
        for response in paginator.paginate(InstanceIds=instanceids):
            for reservations in response['Reservations']:
                for instance in reservations['Instances']:
                    instance['Tags'] = convert_list_to_dict(instance['Tags'])
                    instances.append(instance)
    except ClientError as error:
        logging.warn(error)
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
        self.alarm_names = set()
        self.metric_map = {}

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
            self.alarm_names.add(alarm['AlarmName'])
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

            if alarm['Namespace'] not in self.metric_map:
                self.metric_map[alarm['Namespace']] = set()
            self.metric_map[alarm['Namespace']].add(metricname)
        self._write()

    def _write(self):
        with open('metric-map.json', 'w') as outfile:
            for key in self.metric_map:
                self.metric_map[key] = list(self.metric_map[key])
            outfile.write(json.dumps(self.metric_map, indent=4))

        logging.info('Unique Namespaces: %s', ', '.join(self.namespaces))
        logging.info('Unique MetricNames: %s', ', '.join(self.metricnames))
        logging.info('Unique Instances: %s', len(self.alarms.keys()))
        logging.debug('Unique Instances: %s', ', '.join(self.alarms.keys()))
        logging.info('Found %s total alarms', self.alarm_count)


DESIRED_ALARMS = {
    "AWS/EC2": {
        # "NetworkOut": {},
        # "StatusCheckFailed_System": {},
        "StatusCheckFailed": {},
        "CPUUtilization": {},
    },
    "CWAgent": {
        "procstat_lookup_pid_count": {},
    },
    "System/Windows": {
        "WindowsDiskFreeSpace": {
            "C:": {},
            "F:": {},
            "X:": {},
            "D:": {},
            "I:": {},
        },
        "MemoryUtilization": {},
    },
    "System/Linux": {
        "MemoryUtilization": {}
    }
}


def missing_alarms_(instance_map, client, get_alarms):
    missing_alarms = {}
    for instance_id, instance_name in instance_map.items():
        m_a = process_desired_alarms(
            instance_id, instance_name, get_alarms, client)
        if m_a:
            missing_alarms[instance_id] = m_a
    with open('missing_alarms.json', 'w') as outfile:
        outfile.write(json.dumps(missing_alarms, indent=4))


def process_desired_alarms(instance_id, instance_name, get_alarms, client):
    available_metrics = {}
    for m in client.list_metrics(
            Dimensions=[{'Name': 'InstanceId', 'Value': instance_id}])['Metrics']:
        if m['Namespace'] not in available_metrics:
            available_metrics[m['Namespace']] = {}
        if m['MetricName'] not in available_metrics[m['Namespace']]:
            available_metrics[m['Namespace']][m['MetricName']] = {}
        dimensions = convert_list_to_dict(m['Dimensions'], 'Name', 'Value')
        if dimensions.get('instance'):
            available_metrics[m['Namespace']][m['MetricName']][dimensions.get('instance')] = {}
    missing_alarms = []
    for namespace in DESIRED_ALARMS:
        for metricname in DESIRED_ALARMS[namespace]:
            if DESIRED_ALARMS[namespace][metricname]:
                for disk in DESIRED_ALARMS[namespace][metricname]:
                    alarm_name = '{}-{}-{}-{}'.format(instance_id, instance_name, disk, metricname)
                    if (alarm_name not in get_alarms.alarm_names and
                            namespace in available_metrics and
                            metricname in available_metrics[namespace] and
                            disk in available_metrics[namespace][metricname]):
                        missing_alarms.append(alarm_name)
            else:
                alarm_name = '{}-{}-{}'.format(instance_id, instance_name, metricname)
                if (alarm_name not in get_alarms.alarm_names and
                        namespace in available_metrics and
                        metricname in available_metrics[namespace]):
                    missing_alarms.append(alarm_name)
    return missing_alarms


def malformed_alarms_(get_alarms, instance_map):
    """Write out the alarms which fail to conform to our naming scheme."""
    multiple_alarm_count = 0
    strict_malformed_alarms = []
    malformed_alarms = []
    alarms_no_instance_exists = []
    multiple_alarms = {}

    for instanceid in get_alarms.alarms:
        for namespace in get_alarms.alarms[instanceid]:
            for metricname in get_alarms.alarms[instanceid][namespace]:
                for alarm in get_alarms.alarms[instanceid][namespace][metricname]:
                    alarm_name_parts = alarm['AlarmName'].split('-')
                    instance_name = instance_map.get(instanceid) or 'undefined'
                    if instanceid not in instance_map:
                        alarms_no_instance_exists.append(alarm)

                    if (instanceid in instance_map and
                            not alarm['AlarmName'].lower().startswith('{}-{}'.format(
                                instanceid, instance_name.lower())) and
                            alarm_name_parts[-1] in ALLOWED_SUFFIXES):
                        strict_malformed_alarms.append(alarm)

                    if instanceid in instance_map:
                        logging.debug('%s: %s', alarm['AlarmName'], len(alarm_name_parts))
                        # i-ffb08b38-AwOr-PdTibEms02-StatusCheckFailed
                        if '-'.join(alarm_name_parts[0:2]) == instanceid:
                            if (
                                    (alarm_name_parts[-1] in ALLOWED_SUFFIXES_3 and
                                     len(alarm_name_parts) <= 3) or
                                    (alarm_name_parts[-1] in ALLOWED_SUFFIXES_4 and
                                     len(alarm_name_parts) <= 4)):
                                malformed_alarms.append(alarm)

                if len(get_alarms.alarms[instanceid][namespace][metricname]) > 1:
                    multiple_alarm_count += 1

                    if instanceid not in multiple_alarms:
                        multiple_alarms[instanceid] = {}

                    if namespace not in multiple_alarms[instanceid]:
                        multiple_alarms[instanceid][namespace] = {}

                    if metricname not in multiple_alarms[instanceid][namespace]:
                        multiple_alarms[instanceid][namespace][metricname] = []

                    multiple_alarms[instanceid][namespace][metricname].append(
                        [a['AlarmName']
                         for a in get_alarms.alarms[instanceid][namespace][metricname]])

    logging.info('Found %s Alarms without instances existing for them',
                 len(alarms_no_instance_exists))
    with open('alarms_no_instance_exists.txt', 'w') as outfile:
        outfile.write(
            "\n".join([
                a['AlarmName']
                for a in sorted(
                    alarms_no_instance_exists, key=lambda x: x['AlarmName'])]))

    logging.info('Found %s Alarms which do not follow i-X-instancename strict',
                 len(strict_malformed_alarms))
    with open('strict_malformed_alarms.txt', 'w') as outfile:
        outfile.write(
            "\n".join([
                a['AlarmName']
                for a in sorted(
                    strict_malformed_alarms, key=lambda x: x['AlarmName'])]))

    logging.info('Found %s Alarms which do not follow i-X-instancename loose',
                 len(malformed_alarms))
    with open('malformed_alarms.txt', 'w') as outfile:
        outfile.write(
            "\n".join([
                a['AlarmName']
                for a in sorted(
                    malformed_alarms, key=lambda x: x['AlarmName'])]))

    logging.info('Found %s alarms with duplicate entries', multiple_alarm_count)
    with open('multiple_alarms.json', 'w') as outfile:
        outfile.write(json.dumps(multiple_alarms, indent=4))

def managed_alarms_munge(instances, get_alarms):
    """Discover from our list of alarms which instances are missing alarms."""
    instances_missing_alarms = [i for i in instances if i not in get_alarms.alarms]
    logging.info('Instances missing alarms(%s)', len(instances_missing_alarms))
    with open('instances-missing-alarms.txt', 'w') as outfile:
        outfile.write("\n".join(instances_missing_alarms))

    managed_instances_missing_alarms = [
        i
        for i, v in instances.items()
        if i not in get_alarms.alarms and
        v['Tags'].get('Managed', 'Yes').lower() == 'yes']
    logging.info('Managed Instances missing alarms(%s)', len(managed_instances_missing_alarms))
    with open('managed-instances-missing-alarms.txt', 'w') as outfile:
        outfile.write("\n".join(managed_instances_missing_alarms))


def main():
    """Main."""
    client = boto3.client('cloudwatch', REGION)
    ec2_client = boto3.client('ec2', REGION)
    get_alarms = GetAlarms(client)
    get_alarms.get_alarms()
    instances = describe_all_instances(ec2_client)
    instance_map = get_instance_map(instances)
    malformed_alarms_(get_alarms, instance_map)
    managed_alarms_munge({i['InstanceId']: i for i in instances}, get_alarms)
    missing_alarms_(instance_map, client, get_alarms)


if __name__ == '__main__':
    main()