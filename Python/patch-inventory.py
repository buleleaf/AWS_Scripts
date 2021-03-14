#!/usr/bin/env python3
"""Executes a SSM Document which captures in S3 a list of all installed packages for selected hosts."""
import time
import logging
import os
import csv
import datetime
import json
import boto3
from botocore.exceptions import ClientError
from tabulate import tabulate
from utils import (
    configure_logging, SSMParamStoreKey, SlackMessage, json_dumps,
    push_to_queue, chunk_list, put_file_to_s3, make_s3_url,
    retrieve_json_from_s3)
import rpm_vercmp
try:
    from io import StringIO
except ImportError:
    try:
        from cStringIO import StringIO
    except ImportError:
        from StringIO import StringIO

logging.getLogger('boto3').setLevel(logging.ERROR)
logging.getLogger('botocore').setLevel(logging.ERROR)

QUEUE_URL = os.environ.get('QUEUE_INV_URL')
# i-0781ab28c094092a9 - out of disk
# BLACKLISTED_INSTANCES = ('i-0781ab28c094092a9',)
BLACKLISTED_INSTANCES = ('',)
AREF = '<a href="{}">{}</a>'


def _bool_check_command_status(client, command_info, instance_id):
    """Retrieve status of execute SSM RunCommand."""
    command_status = _check_command_status(client, command_info['CommandId'],
                                           instance_id)
    return command_status['Status'] in ('Pending', 'InProgress', 'Delayed')


def _check_command_status(client, command_id, instance_id):
    """Retrieve details of execute SSM RunCommand."""
    logging.debug('Command Id: %s; InstanceId: %s', command_id, instance_id)
    invocations = client.list_command_invocations(
        CommandId=command_id,
        InstanceId=instance_id)['CommandInvocations']
    if invocations:
        return invocations[0]
    return {'Status': ['Pending'], 'InstanceId': instance_id,
            'CommandId': command_id,
            'Error': 'Unable to list command invocation.'}


def send_runcommand(ssm_client, **kwargs):  # noqa
    """Takes in a boto3 session and some kwargs, splits list of instances
    into groups for 50, sends RunCommand, and returns a list of the
    responses.
    """
    doc = 'AWS-RunShellScript'
    response = []
    chunks = chunk_list(kwargs['instances'], 50)  # max 50 instances
    for chunk in chunks:  # iterate over chunks of 50 instances
        response.append(ssm_client.send_command(
            DocumentName=doc,
            InstanceIds=chunk,
            Parameters={  # value must be a list
                'commands': [
                    "#!/bin/bash",
                    'bucket={bucket}'.format(**kwargs),
                    'instance_id=$(curl -s http://169.254.169.254/latest/meta-data/instance-id)',
                    'echo $instance_id $bucket',
                    'if type -t rpm >/dev/null 2>&1;then',
                    ('''    pkg_list=$(rpm -qa --queryformat '"%-30{NAME}": '''
                     '''"%10{VERSION}-%20{RELEASE}",' | sed -e 's~,$~~'  | tr -d ' ')'''),
                    '    echo "{${pkg_list}}" | \\',
                    ('''    python -c 'import json, sys; print(json.dumps('''
                     '''json.loads(sys.stdin.read()), indent=4))' > pkg_list.json'''),
                    '    echo Retrieved package list from rpm',
                    'fi',
                    'if type -t dpkg >/dev/null 2>&1;then',
                    '    echo "Found debian"',
                    'fi',
                    'test -e pkg_list.json || echo unable to find pkg_list.json',
                    'aws s3 cp pkg_list.json s3://$bucket/patching-state/%s/${instance_id}.json' % (
                        kwargs['delta_date']),
                    'echo Completed Export',
                ],
            },
            OutputS3BucketName=kwargs['bucket'],
            OutputS3KeyPrefix='command-output',
            TimeoutSeconds=kwargs['timeout'],
            MaxErrors='10',
        )['Command'])  # appends command return to a list for return

    return response


def _describe_instance(client, instance):
    try:
        client.describe_instances(InstanceIds=[instance])
    except ClientError as error:
        logging.error(error)
        if error.response['Code']['Message'] in ('InvalidInstanceID.NotFound', 'InvalidInstanceID.Malformed'):
            logging.error('%s instance is not valid.', instance)
        else:
            raise
    else:
        return True
    return False


def _is_ssm_managed(client, instance):
    try:
        r = client.describe_instance_information(Filters=[{'Key': 'InstanceIds', 'Values': [instance]}])
        logging.debug(r.get('InstanceInformationList', []))
    except Exception as error:
        logging.error(error)
        raise
    else:
        if r.get('InstanceInformationList'):
            return True
    return False


def _get_instance_pairs(s3_client, ec2_client, ssm_client, bucket, key):
    logging.info('Retrieving instance pairs from s3://%s/%s', bucket, key)
    resp = s3_client.get_object(Bucket=bucket, Key=key)
    csv_body = StringIO(resp['Body'].read().decode('utf-8'))

    reader = csv.DictReader(csv_body)
    instances = {}

    for row in reader:
        if row.get('SourceInstanceId'):
            for instance in (row.get('SourceInstanceId'), row.get('InstanceId')):
                if not (_describe_instance(ec2_client, instance) and
                        _is_ssm_managed(ssm_client, instance)):
                    continue
            instances[row.get('InstanceId')] = row.get('SourceInstanceId')
    return instances


def _get_instances(s3_client, ec2_client, ssm_client, bucket, key):
    logging.info('Retrieving instance list from s3://%s/%s', bucket, key)
    resp = s3_client.get_object(Bucket=bucket, Key=key)
    csv_body = StringIO(resp['Body'].read().decode('utf-8'))

    reader = csv.DictReader(csv_body)
    instances = set()

    for row in reader:
        if row.get('SourceInstanceId'):
            for instance in (row.get('SourceInstanceId'), row.get('InstanceId')):
                if (_describe_instance(ec2_client, instance) and
                        _is_ssm_managed(ssm_client, instance) and
                        instance not in BLACKLISTED_INSTANCES):
                    instances.add(instance)
    return instances


def _process_delta_pair(prod_instance_id, source_instance_id, bucket, delta_date, s3_client):

    def key_paths(source_instance_id, prod_instance_id):
        """Form S3 keys based on variables."""
        non_prod_pkg_list_key = 'patching-state/{}/{}.json'.format(delta_date, source_instance_id)
        prod_pkg_list_key = 'patching-state/{}/{}.json'.format(delta_date, prod_instance_id)
        mismatch_versions_key = 'patching-state/{}/{}/version-mismatch.json'.format(delta_date, prod_instance_id)
        not_on_prod_key = 'patching-state/{}/{}/not-on-prod.csv'.format(delta_date, prod_instance_id)
        out_of_date_key = 'patching-state/{}/{}/out-of-date.csv'.format(delta_date, prod_instance_id)
        return non_prod_pkg_list_key, prod_pkg_list_key, mismatch_versions_key, not_on_prod_key, out_of_date_key

    def format_str(instance_id, pkg_list):
        return instance_id if pkg_list else instance_id + ' (Missing pkg list)'

    logging.info('Processing pair %s and %s', prod_instance_id, source_instance_id)
    (non_prod_pkg_list_key, prod_pkg_list_key,
     mismatch_versions_key, not_on_prod_key, out_of_date_key) = key_paths(
         source_instance_id, prod_instance_id)

    prod_s3_url = make_s3_url(bucket, prod_pkg_list_key)
    non_prod_s3_url = make_s3_url(bucket, non_prod_pkg_list_key)

    prod_pkg_list = retrieve_json_from_s3(s3_client, bucket, prod_pkg_list_key)
    nonprod_pkg_list = retrieve_json_from_s3(s3_client, bucket, non_prod_pkg_list_key)

    if not prod_pkg_list or not nonprod_pkg_list:
        logging.error('Missing pkg list')
        return {
            'Prod Instance': AREF.format(
                prod_s3_url, format_str(prod_instance_id, prod_pkg_list)),
            'Non-Prod Instance': AREF.format(
                non_prod_s3_url, format_str(
                    source_instance_id, nonprod_pkg_list)),
            'Updates Needed': '',
            'Not installed on Prod': '',
            'Version Mismatch': '',
        }

    # not on prod but installed on nonprod
    not_on_prod = set(nonprod_pkg_list).difference(set(prod_pkg_list))

    # version mismatch
    mismatch_versions = {}
    old_versions = []
    for pkg in nonprod_pkg_list:

        if pkg in prod_pkg_list and rpm_vercmp.vercmp(nonprod_pkg_list[pkg], prod_pkg_list[pkg]) == 1:
            mismatch_versions[pkg] = {'prod': prod_pkg_list[pkg], 'nonprod': nonprod_pkg_list[pkg]}
            old_versions.append(pkg + "-" + nonprod_pkg_list[pkg])

    # Uploading files to s3
    put_file_to_s3(s3_client, '\n'.join(list(not_on_prod)), bucket,
                   not_on_prod_key)
    put_file_to_s3(s3_client, '\n'.join(list(old_versions)), bucket,
                   out_of_date_key)
    put_file_to_s3(s3_client, json.dumps(mismatch_versions, indent=4), bucket,
                   mismatch_versions_key)

    return {
        'Prod Instance': AREF.format(prod_s3_url, prod_instance_id),
        'Non-Prod Instance': AREF.format(non_prod_s3_url, source_instance_id),
        'Updates Needed': AREF.format(
            make_s3_url(bucket, out_of_date_key), 'Out of date packages'),
        'Not installed on Prod': AREF.format(
            make_s3_url(bucket, not_on_prod_key), 'Not installed on Prod'),
        'Version Mismatch': AREF.format(
            make_s3_url(bucket, mismatch_versions_key), 'Version Mismatch'),
    }


def _make_html_report(table_report):
    html_report = '''<html>
    <head>
        <title>Delta Inventory Report</title>
        <style>
            table, th, td {
              border: 1px solid black;
              border-collapse: collapse;
            }
        </style>
    </head>
    <body>
        <h1>Delta Inventory Report</h1>
        <p>Inventory report on instances in the prod patch list which do have a
            source instance and compare the list of installed packages on both
            hosts for differences.
        </p>'''
    html_report += tabulate(table_report, tablefmt='html')
    html_report += '''
        <p>Note: Reasons for missing change list are the command failed to run
            or the instance isn't managed by SSM.
        </p>
    </body>
</html>'''
    return html_report


def inventory_hosts(event, context):
    """Inventory Hosts."""
    bucket = event.get('s3_bucket', os.getenv('BUCKET'))
    s3_key = event.get('s3_key', os.getenv('CSV_KEY'))
    delta_date = event.get('delta_date', datetime.date.today().isoformat())
    session = boto3.session.Session()
    ec2_client = session.client('ec2')
    s3_client = session.client('s3')
    ssm_client = session.client('ssm')
    instances = list(_get_instances(s3_client, ec2_client, ssm_client, bucket, s3_key))
    logging.info(instances)
    commands = send_runcommand(ssm_client, instances=instances, timeout=3600, bucket=bucket, delta_date=delta_date)
    commandids = [c['CommandId'] for c in commands]
    logging.info('Commands: %s', ', '.join(commandids))
    queue_data = event.copy()
    queue_data['action'] = 'inventory-wait'
    queue_data['commands'] = commands
    queue_data['wait-count'] = 0
    push_to_queue(QUEUE_URL, queue_data)
    return queue_data


def command_complete(event, context):
    """Check status of in progress patching."""
    queue_data = event.copy()
    client = boto3.client('ssm')
    command_statuses = [
        _bool_check_command_status(client, command, instance_id)
        for command in event['commands']
        for instance_id in command['InstanceIds']]
    logging.info('Command Statuses(all false will start reporting): %s',
                 command_statuses)

    # if not any of our commands are still pending
    kwargs = {}
    if not any(command_statuses):
        queue_data['action'] = 'report-delta'
    else:
        queue_data['wait-count'] += 1
        kwargs['DelaySeconds'] = 60
    push_to_queue(QUEUE_URL, queue_data, **kwargs)
    return queue_data


def make_delta(event, context):
    """Calculate delta from inventory lists."""
    bucket = event.get('s3_bucket', os.getenv('BUCKET'))
    s3_key = event.get('s3_key', os.getenv('CSV_KEY'))
    logging.info('Retrieving patching csv from bucket %s', bucket)
    session = boto3.session.Session()
    s3_client = session.client('s3')
    instances = _get_instance_pairs(s3_client, session.client('ec2'), session.client('ssm'), bucket, s3_key)
    logging.info(instances)
    table_report = [
        _process_delta_pair(prod_instance_id, source_instance_id, bucket,
                            event['delta_date'], s3_client)
        for prod_instance_id, source_instance_id in instances.items()]
    html_report = _make_html_report(table_report)

    report_key = 'patch-delta/delta-report-{}.html'.format(datetime.datetime.now().isoformat(timespec='seconds'))
    put_file_to_s3(s3_client, html_report, bucket, report_key)
    report_url = make_s3_url(bucket, report_key)
    logging.info('Report URL: %s', report_url)
    slack_config = SSMParamStoreKey(
        os.environ.get('DELTA_SLACK_CONFIG')
    ).get(decrypt=True)['Parameter']['Value']
    msg = {'text': 'Delta Inventory Report', 'color': '#439FE0', 'actions': [{
        'type': 'button',
        'text': 'Report',
        'style': 'primary',
        'url': report_url
    }]}
    SlackMessage(**msg).send(slack_config)
    return True


def init_inventory_hosts(event, context):
    """Check for schedules which we need to run inventory for.

    Pull schedules, check if any schedules are happening within a week that
    we've not done inventory for.
    """
    def check_s3_prefix(bucket, prefix):
        client = boto3.client('s3')
        logging.info('Checking for objects at s3://%s/%s', bucket, prefix)
        response = client.list_objects_v2(Bucket=bucket, Prefix=prefix)
        logging.info(response)
        return bool(response.get('Contents'))
    bucket = os.getenv('BUCKET')
    ssm_key = os.environ.get('SCHEDULE_SSM_KEY')

    ssm_schedule = SSMParamStoreKey(ssm_key)
    ssm_schedules = ssm_schedule.get(decrypt=True)
    logging.debug(ssm_schedules)
    logging.info(ssm_schedules['Parameter']['Value'])
    schedules = json.loads(ssm_schedules['Parameter']['Value'])
    for schedule in schedules:
        run_inventory = False
        run_time = datetime.datetime.utcfromtimestamp(schedule['run_time'])
        delta_date = run_time - datetime.timedelta(days=2)
        logging.info(delta_date)
        delta_date = delta_date.date()
        logging.info(delta_date)
        if 'delta-date' in schedule:
            delta_date = datetime.date.fromisoformat(schedule['delta-date'])
        logging.info('Found schedule, %s to be executed at %s',
                     schedule['patch_name'],
                     run_time.isoformat())
        prefix_exists = check_s3_prefix(
            bucket,
            'patching-state/{}'.format(delta_date.isoformat()))
        logging.debug('Today: %s; Week Before schedule: %s', datetime.datetime.utcnow(), delta_date)
        logging.info(datetime.date.today())
        logging.info(delta_date)
        if (datetime.date.today() >= delta_date and
                schedule['mode'] in ('prod', ) and
                not prefix_exists):
            run_inventory = True
        if run_inventory:
            s3_bucket, s3_key = schedule['patch_list'].split(':', 1)
            queue_data = {
                'action': 'inventory-hosts',
                'delta_date': delta_date.isoformat(),
                's3_key': s3_key,
                's3_bucket': s3_bucket,
            }
            push_to_queue(QUEUE_URL, queue_data)
            return queue_data
    return True


def lambda_handler(event, context):
    """Lambda function entry point."""
    configure_logging({'aws_request_id': context.aws_request_id})
    main(event, context)


def main(event, context):
    """Main."""
    logging.info('Using queue %s', QUEUE_URL)
    logging.debug(event)
    actions = {
        'init-inventory-hosts': init_inventory_hosts,
        'inventory-hosts': inventory_hosts,
        'inventory-wait': command_complete,
        'report-delta': make_delta,
    }
    if not event.get('Records'):
        logging.error('No Records key.')
        logging.error(event)
    # We should have only one record per event, but sanity
    for record in event.get('Records', []):  # if we don't have
        logging.debug(json_dumps(record))
        data = json.loads(record['body'])
        logging.info(data)
        if data['action'] in actions:
            return json_dumps(actions[data['action']](data, context))
        raise Exception('Unknown action {}.'.format(data['action']))


if __name__ == '__main__':
    configure_logging({'aws_request_id': "local"})
    os.environ['AWS_DEFAULT_REGION'] = 'us-west-2'
    os.environ['BUCKET'] = 'edwards-asadmin-patching-bucket-us-west-2'
    os.environ['SCHEDULE_SSM_KEY'] = '/config/patching/schedule'
    os.environ['SLACK_CONFIG'] = '/onica/slack/webhook'
    resp = {'action': 'init-inventory-hosts'}
    while resp != True:
        resp = main({'Records': [{'body': json_dumps(resp)}]}, None)
        time.sleep(10)
