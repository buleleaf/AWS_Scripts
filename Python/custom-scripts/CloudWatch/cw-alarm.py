# pip install boto3

import boto3

cloudwatch_client = boto3.client('cloudwatch', region_name='us-west-2')

response = cloudwatch_client.put_metric_alarm(
    OKActions=[
        'arn:aws:sns:us-west-2:590992000271:freshservice_monitor'
    ],
    AlarmActions=[
        'arn:aws:sns:us-west-2:590992000271:freshservice_monitor'
    ],
    AlarmDescription='{ "region": "us-west-2", "managed": "Yes", "account_id": "590992000271", "account_name": "asadmin"}',
    AlarmName='i-c99b88d1-AWORPDPLMFIL01-F:-LogicalDisk%FreeSpace',
    ComparisonOperator='LessThanThreshold',
    EvaluationPeriods=4,
    InsufficientDataActions=[],
    MetricName='LogicalDisk % Free Space',
    Namespace='System/Windows',
    Period=300,
    Statistic='Average',
    Threshold=15,
    TreatMissingData='breaching',
    Dimensions=[
        {
            'Name': 'InstanceId',
            'Value': 'i-c99b88d1'
        },
        {
            'Name': 'instance',
            'Value': 'F:'
        },
        {
            'Name': 'objectname',
            'Value': 'LogicalDisk'
        }
    ]
)