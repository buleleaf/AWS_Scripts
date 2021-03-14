#!/usr/bin/env python
"""Start patching process for environments."""

import pickle
from json import JSONEncoder
import csv
import json
import datetime
import os
import logging
from collections import defaultdict
import boto3
from botocore.vendored import requests
import botocore
from hashlib import sha1
try:
    from StringIO import StringIO
except ImportError:
    from cStringIO import StringIO

FORMAT = '%(asctime)-15s %(levelname)s %(module)s.%(funcName)s %(message)s'
DATEFMT = "%Y-%m-%d %H:%M:%S"
logging.basicConfig(level=logging.INFO, format=FORMAT, datefmt=DATEFMT)
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)

QUEUE_URL = os.environ.get('QUEUE_URL')
SSM_KEY = os.environ.get('SCHEDULE_SSM_KEY')
AWS_REGION = os.environ.get('AWS_REGION')


class SlackMessage(object):  # pylint: disable=too-few-public-methods
    """Class for handling Slack messages."""

    def __init__(self, **kwargs):
        """Class for constructing and sending a Slack message.

        KWARGS:
            fallback -- Required plain-text summary of the attachment.
            color -- good, warning, danger, or a hex value
            author_name -- optional
            author_link -- optional
            author_icon -- optional
            title -- bold text near the top of a message
            title_link -- optional to turn title into hyperlink
            text -- option text to appear in message
            fields {list} -- optional list of dictionaries
                title -- bold text above value text
                value -- text field
                short -- option booleon value to show side-by-side
            image_url -- optional url to image
            thumb_url -- optional
            footer -- optional footer message
            footer_icon -- optional footer icon
            ts -- optional timestamp

        """
        self.title = kwargs.get('title', 'Patching Notification')
        self.fallback = kwargs.get('fallback', 'Patching Notification')

        for key, val in kwargs.items():
            setattr(self, key, val)

    def send(self, endpoint):  # noqa
        """Sends Slack message.

        Arguments:
            endpoint {string} -- Slack webhook url endpoint

        """
        payload = {'attachments': [self.__dict__]}
        return requests.post(endpoint, json=payload)


class PythonObjectEncoder(JSONEncoder):
    """Python Object to JSON encoder."""

    def default(self, obj):
        """default."""
        if isinstance(obj, (datetime.datetime, datetime.date)):
            return obj.isoformat()
        elif isinstance(obj, (list, dict, str, unicode, int, float, bool, type,
                              type(None))):
            return JSONEncoder.default(self, obj)
        logging.warning(
            "Unable to find matching encoder for type %s. Using pickle",
            str(type(obj)),
        )
        return {"_python_object": pickle.dumps(obj)}


class SSMParamStoreKey(object):
    """Interface for dealing with AWS SSM Parameter Store Keys."""

    def __init__(self, path):
        """Init."""
        self._client = boto3.client('ssm', region_name=AWS_REGION)
        self._path = path

    def get(self, decrypt=False):
        """Retrieve Key."""
        return self._client.get_parameter(Name=self._path,
                                          WithDecryption=decrypt)

    def set(self, value, encrypt=None):
        """Set Key."""
        if encrypt:
            return self._client.put_parameter(
                Name=self._path,
                Value=value,
                Type='SecureString',
                KeyId=encrypt)
        return self._client.put_parameter(
            Name=self._path,
            Value=value,
            Type='String',
            Overwrite=True)


SLACK_CONFIG = SSMParamStoreKey(
    os.environ.get('SLACK_CONFIG')
).get(decrypt=True)['Parameter']['Value']


def push_to_queue(sqs_queue, payload):
    """Push data to sqs queue."""
    client = boto3.client('sqs')
    return client.send_message(
        QueueUrl=sqs_queue,
        MessageBody=json.dumps(payload))


def get_patch_list(s3_url, region_name=AWS_REGION):
    """Retrieve Patch list from S3."""
    client = boto3.client('s3')
    bucket, path = s3_url.split(':', 1)
    try:
        resp = client.get_object(Bucket=bucket, Key=path)
    except botocore.exceptions.ClientError as error:
        # more than likely GetObject operation: Access Denied
        LOGGER.error('Path to csv: %s/%s', bucket, path)
        LOGGER.error(error)
        return []

    if not resp:
        LOGGER.error(resp)

    region_sort = defaultdict(list)
    csv_body = StringIO(resp['Body'].read().decode('utf-8'))
    LOGGER.debug(type(csv_body))
    LOGGER.debug(csv_body)
    reader = csv.DictReader(csv_body)

    for inst in reader:
        logging.info(inst)
        region = region_name
        if 'Region' in inst and inst['Region']:
            region = inst['Region']
        region_sort[region].append(inst)

    results = region_sort[region]
    LOGGER.info(results)
    return results


def validate_schedule(schedule):
    """Validate Schedule has requisite parts."""
    if not ('run_time' in schedule and isinstance(schedule['run_time'],
                                                  int)):
        LOGGER.error('Invalid run_time. Skipping schedule.')
        return False
    if 'patch_name' not in schedule:
        LOGGER.error('Schedule is missing patch name. '
                     'Patching will not happen for this schedule.')
        return False
    if 'patch_list' in schedule and ':' not in schedule['patch_list']:
        LOGGER.error('Invalid s3 path.'
                     'Patching will not happen for this schedule.')
        return False
    if 'mode' not in schedule:
        LOGGER.error('Missing schedule mode. Skipping.')
        return False

    run_time = datetime.datetime.utcfromtimestamp(schedule['run_time'])
    LOGGER.info('Found schedule, %s to be executed at %s',
                schedule['patch_name'],
                run_time.isoformat())
    if datetime.datetime.utcnow() < run_time:
        LOGGER.info('Execution time is in the future for %s. '
                    'Skipping.', schedule['patch_name'])
        return False

    if 'prod' in schedule['mode']:
        if 'dev-patch-date' not in schedule:
            LOGGER.error('Prod patching requires "dev-patch-date".')
            return False
        try:
            datetime.datetime.strptime(schedule['dev-patch-date'], '%Y-%m-%d')
        except Exception as error:
            LOGGER.error(error)
            LOGGER.error('Dev Patch date is invalid. Value we parsed is: %s',
                         schedule['dev-patch-date'])
            return False

    return True


def instance_validation(instances, mode, patch_name):
    """Validate all instances conform with required fields."""
    if not instances:
        LOGGER.error('Found no instances to patch. Skipping.')
        return False
    required_fields = ['InstanceId', 'Region', 'InstanceName']
    if 'prod' in mode:
        required_fields.extend(['SourceInstanceName', 'IpAdress',
                                'Authentication', 'SourceInstanceId'])
    invalid_instances = []
    for inst in instances:
        missing_fields = []
        for field in required_fields:
            if field not in inst:
                LOGGER.error('%s is missing from "%s".', field,
                             json.dumps(inst, cls=PythonObjectEncoder))
                missing_fields.append(field)
        if missing_fields:
            invalid_instances.append(inst)
    if invalid_instances:
        LOGGER.error('We have instances with missing data. '
                     'Schedule is invalid.')
        return False
    client = boto3.client('ec2')
    try:
        client.describe_instances(
            InstanceIds=[i['InstanceId'] for i in instances])
    except botocore.exceptions.ClientError as error:
        LOGGER.error(error)
        SlackMessage(**{
            'text': ('Invalid Instances found for {} schedule. '
                     'Please check csv.\n').format(patch_name),
            'color': '#FF0000'
        }).send(SLACK_CONFIG)
        return False
    return True


def lambda_handler(event, context):  # pylint disable=W0613
    """Main."""
    ssm_schedule = SSMParamStoreKey(SSM_KEY)
    ssm_schedules = ssm_schedule.get(decrypt=True)
    LOGGER.debug(ssm_schedules)
    LOGGER.info(ssm_schedules['Parameter']['Value'])

    schedules = json.loads(ssm_schedules['Parameter']['Value'])
    new_schedules = []
    for schedule in schedules:
        if not validate_schedule(schedule):
            new_schedules.append(schedule)
            continue

        instances = get_patch_list(schedule['patch_list'],
                                   schedule.get('region', AWS_REGION))

        if not instance_validation(instances, schedule['mode'],
                                   schedule['patch_name']):
            new_schedules.append(schedule)
            continue

        queue_data = schedule.copy()
        queue_data['action'] = 'create-snap'
        queue_data['instances'] = instances
        del queue_data['patch_list']
        LOGGER.info(queue_data)

        push_to_queue(QUEUE_URL, queue_data)

    # Update SSM Param with the new set of schedules.
    json_old_schedule = ssm_schedules['Parameter']['Value']
    json_new_schedule = json.dumps(new_schedules)
    digest_new = sha1(json_new_schedule).hexdigest()
    digest_old = sha1(json_old_schedule).hexdigest()
    if digest_new != digest_old:
        LOGGER.info('Updating schedule param')
        ssm_schedule.set(json_new_schedule)
    else:
        LOGGER.info('Detected same digests of the schedules.')
