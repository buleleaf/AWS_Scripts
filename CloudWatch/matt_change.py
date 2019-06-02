"""Gather CloudWatch metric details and alarms for a ec2 tag."""

import boto3
import datetime
import argparse
import logging
import json

from operator import itemgetter

logging.basicConfig(level=logging.INFO)
log = logging.getLogger()
log.setLevel(logging.INFO)
logging.getLogger('boto3').setLevel(logging.ERROR)
logging.getLogger('botocore').setLevel(logging.ERROR)

parser = argparse.ArgumentParser(description='Get cloudwatch data from alarm')
parser.add_argument('tag', help='Tag to check instances by')
parser.add_argument('tag_value', help='Tag Value to check instances by')
parser.add_argument('--days', help='How far back to view', default=30)
parser.add_argument('--sample_period', help='period to sample (seconds)', default=300)  # noqa: E501
parser.add_argument('--statechange', help='View state change events', action='store_true')  # noqa: E501
args = parser.parse_args()

# Metrics to Check
included_metrics = ['CPUUtilization', 'DiskWriteOps']
# included_metrics = ['*']

regions = boto3.client('ec2', 'us-east-1').describe_regions()


def fix_metrics_dates(metrics):
    """Return JSON-friendly ordered metric data."""
    datapoints = sorted(metrics, key=itemgetter('Timestamp'))
    for datapoint in datapoints:
        if isinstance(datapoint['Timestamp'], (datetime.datetime, datetime.date)):  # noqa: E501
            datapoint['Timestamp'] = datapoint['Timestamp'].isoformat()
    return datapoints


def get_tag(obj, key):
    """
    Get tag value from an instance dict by specified key.

        obj (dict) = One resource
        key (str) = Case sensitive tag-key

    """
    return {
        t['Key']: t['Value'] for t in obj['Tags']if t['Key'] == key
    }.get(key)


report = {}
for region in regions['Regions']:
    region_name = region['RegionName']
    cw = boto3.client('cloudwatch', region_name)
    ec2 = boto3.client('ec2', region_name)
    log.info('Checking for instances in {}'.format(region_name))
    paginator = ec2.get_paginator('describe_instances')
    response_iterator = paginator.paginate(
        Filters=[
            {
                'Name': 'tag:{}'.format(args.tag),
                'Values': [args.tag_value]
            },
        ],
        MaxResults=1000)


    #if len(instances) > 0:
    report[region_name] = {}
    #    log.info('found {} instances'.format(len(instances[0]['Instances'])))
    for page in response_iterator:
        for reservation in page['Reservations']:
            for instance in reservation['Instances']:
    #for instance in instances:
        #instance = instance['Instances'][0]
                instance_id = instance['InstanceId']
                report[region_name][instance_id] = {}
                report[region_name][instance_id]['Metadata'] = {}
                if get_tag(instance, 'Name'):
                    report[region_name][instance_id]['Metadata']['Name'] = get_tag(instance, 'Name')  # noqa: E501
                else:
                    report[region_name][instance_id]['Metadata']['Name'] = instance_id  # noqa: E501
                dim_filter = [{'Name': 'InstanceId', 'Value': instance_id}]
                metrics = cw.list_metrics(
                    Dimensions=dim_filter
                )

                for metric in metrics['Metrics']:
                    if metric['MetricName'] in included_metrics or included_metrics[0] == '*':  # noqa: E501
                        report[region_name][instance_id][metric['MetricName']] = {}
                        report[region_name][instance_id][metric['MetricName']]['Datapoints'] = []  # noqa: E501
                        datapoints = []
                        log.info('processing metric {} for instance {}'.format(
                            metric['MetricName'],
                            instance['InstanceId']
                        ))
                        metric_window_seconds = 1440 * args.sample_period
                        metric_request_seconds = int(args.days) * 24 * 60 * 60
                        log.info('Maximum request window for sample is {} seconds. requesting {} seconds'.format(  # noqa: E501
                            metric_window_seconds,
                            metric_request_seconds))

                        end = datetime.datetime.utcnow()

                        while metric_request_seconds > 0:
                            if metric_request_seconds < metric_window_seconds:
                                start = end - datetime.timedelta(seconds=int(metric_request_seconds))  # noqa: E501
                            else:
                                start = end - datetime.timedelta(seconds=int(metric_window_seconds))  # noqa: E501
                            log.info('collecting range {} to {}'.format(
                                start.strftime("%Y-%m-%d %H:%M:%S"),
                                end.strftime("%Y-%m-%d %H:%M:%S")
                            ))

                            metric_data = cw.get_metric_statistics(
                                Period=300,
                                StartTime=start,
                                EndTime=end,
                                MetricName=metric['MetricName'],
                                Namespace=metric['Namespace'],
                                Statistics=['Average'],
                                Dimensions=metric['Dimensions']
                            )
                            end = end - datetime.timedelta(seconds=int(metric_window_seconds))  # noqa: E501
                            metric_request_seconds = metric_request_seconds - metric_window_seconds      # noqa: E501
                            datapoints += metric_data['Datapoints']

                        report[region_name][instance_id][metric['MetricName']]['Datapoints'] = fix_metrics_dates(datapoints)  # noqa: E501
                        # if get_tag(instance,"aws:autoscaling:groupName"):
                        #     alarm_dimensions
                        alarms = cw.describe_alarms_for_metric(
                            MetricName=metric['MetricName'],
                            Namespace=metric['Namespace'],
                            Dimensions=metric['Dimensions']
                        )

                        threshold = 0
                        if len(alarms['MetricAlarms']) == 1:
                            log.info("1 alarm identified")
                            threshold = alarms['MetricAlarms'][0]['Threshold']
                            main_alarm = alarms['MetricAlarms'][0]
                        elif len(alarms['MetricAlarms']) > 1:
                            log.info("Multiple alarms identified")
                            for alarm in alarms['MetricAlarms']:
                                if alarm['Threshold'] > threshold and len(alarm['AlarmActions']) != 0:  # noqa: E501
                                    threshold = alarm['Threshold']
                                    main_alarm = alarm
                        else:
                            log.info("No alarms identified")
                            main_alarm = None

                        if main_alarm is not None:
                            report[region_name][instance_id][metric['MetricName']]['Threshold'] = threshold  # noqa: E501
                            report[region_name][instance_id][metric['MetricName']]['Operator'] = main_alarm['ComparisonOperator']  # noqa: E501
                            alarm_hist = cw.describe_alarm_history(
                                AlarmName=main_alarm['AlarmName'],
                                HistoryItemType='StateUpdate',
                                StartDate=datetime.datetime.utcnow() - datetime.timedelta(days=int(args.days)),  # noqa: E501
                                EndDate=datetime.datetime.utcnow(),
                                MaxRecords=100,
                            )

                            next_state = "ALARM"
                            alarm_report = []
                            alarm_hist["AlarmHistoryItems"].reverse()
                            for alarm in alarm_hist["AlarmHistoryItems"]:
                                history = json.loads(alarm["HistoryData"])
                                if history["newState"]["stateValue"] == next_state:
                                    if history["newState"]["stateValue"] == "ALARM":  # noqa: E501
                                        alarm_start = alarm["Timestamp"]
                                        alarm_reason = history["newState"]["stateReason"]  # noqa: E501
                                        alarm_metric = [
                                            history["newState"]["stateReasonData"]["recentDatapoints"][0]  # noqa: E501
                                            if len(history["newState"]["stateReasonData"]["recentDatapoints"]) > 0  # noqa: E501
                                            else [None]
                                        ][0]
                                        next_state = "OK"
                                    elif history["newState"]["stateValue"] == "OK":
                                        alarm_end = alarm["Timestamp"]
                                        alarm_duration = (alarm_end - alarm_start).seconds / 60  # noqa: E501
                                        alarm_report.append({'StartTime': alarm_start.strftime("%c"), 'EndTime': alarm_end.strftime("%c"), 'AlarmDurationMinutes':  alarm_duration, 'AlarmMetric': alarm_metric, 'AlarmReason': alarm_reason})  # noqa: E501
                                        next_state = "ALARM"
                                    else:
                                        log.error(history)
                                else:
                                    next
                            report[region_name][instance_id][metric['MetricName']]['AlarmAnalysis'] = alarm_report  # noqa: E501

js_report = open('metric_report-{}-{}.json'.format(args.tag, args.tag_value), 'w')  # noqa: E501
js_report.write(json.dumps(report))
js_report.close
