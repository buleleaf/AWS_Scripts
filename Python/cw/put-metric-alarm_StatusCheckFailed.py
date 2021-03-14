import json
import boto3
import csv

alarm_name = 'i-397e44fe-AWOR-TSMESWEB02-StatusCheckFailed'
instance_id = 'i-397e44fe'


client = boto3.client('cloudwatch')

response = client.put_metric_alarm(
    AlarmName=alarm_name,
    AlarmDescription="{\n      \"region\": \"us-west-2\", \n      \"managed\": \"Yes\", \n      \"account_id\": \"590992000271\", \n      \"account_name\": \"asadmin\"\n}",
    ActionsEnabled=True,
    OKActions=[
        "arn:aws:sns:us-west-2:590992000271:status-check-failed",
        "arn:aws:sns:us-west-2:590992000271:freshservice_monitor"
    ],
    AlarmActions=[
        "arn:aws:sns:us-west-2:590992000271:status-check-failed",
        "arn:aws:sns:us-west-2:590992000271:freshservice_monitor"
    ],
    MetricName='StatusCheckFailed',
    Namespace='AWS/EC2',
    Statistic='Sum',
    Dimensions=[
        {
            "Name": "InstanceId",
            "Value": instance_id
        }
    ],
    Period=60,
    EvaluationPeriods=5,
    DatapointsToAlarm=5,
    Threshold=1.0,
    ComparisonOperator='GreaterThanOrEqualToThreshold',
    TreatMissingData='notBreaching')