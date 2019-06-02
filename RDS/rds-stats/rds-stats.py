'''
# Ver: 1.0.0
# By: David Mansfield


This script is designed to gather RDS server information based on DB Instance,
DB Software, and Cloudwatch statics based on CPU, Read Latency, and Write Latency.

'''


import boto3
import datetime


region = 'us-east-1'

rds = boto3.client('rds', region_name=region)

dbs = rds.describe_db_instances()

cloudwatch = boto3.client('cloudwatch', region_name=region)

cloudwatch_cpu = cloudwatch.get_metric_statistics(
    Namespace='AWS/RDS',
    MetricName='CPUUtilization',

# Get metric based on specific date and time
    # StartTime=datetime.datetime(2018, 9, 24, 23, 40),
    # EndTime=datetime.datetime(2018, 9, 24, 23, 45),

#  Specify a range between current time and specified time
    StartTime=datetime.datetime.utcnow() - datetime.timedelta(seconds=60),
    EndTime=datetime.datetime.utcnow(),
    Statistics=['Maximum'],
    Period=300,
    Dimensions=[

# Specify the RDS server based on the DB Instance name
        {
            'Name' : 'DBInstanceIdentifier',
            'Value' : 'dmansfieldlab2'

        }
    ],
)

cloudwatch_read_latency = cloudwatch.get_metric_statistics(
    Namespace='AWS/RDS',
    MetricName='ReadLatency',

# Get metric based on specific date and time
    # StartTime=datetime.datetime(2018, 9, 24, 23, 40),
    # EndTime=datetime.datetime(2018, 9, 24, 23, 45),

#  Specify a range between current time and specified time
    StartTime=datetime.datetime.utcnow() - datetime.timedelta(seconds=60),
    EndTime=datetime.datetime.utcnow(),
    Statistics=['Maximum'],
    Period=300,
    Dimensions=[

# Specify the RDS server based on the DB Instance name
        {
            'Name' : 'DBInstanceIdentifier',
            'Value' : 'dmansfieldlab2'

        }

    ],
)

cloudwatch_write_latency = cloudwatch.get_metric_statistics(
    Namespace='AWS/RDS',
    MetricName='WriteLatency',

# Get metric based on specific date and time
    # StartTime=datetime.datetime(2018, 9, 24, 23, 40),
    # EndTime=datetime.datetime(2018, 9, 24, 23, 45),

#  Specify a range between current time and specified time
    StartTime=datetime.datetime.utcnow() - datetime.timedelta(seconds=60),
    EndTime=datetime.datetime.utcnow(),

    Statistics=['Maximum'],
    Period=300,
    Dimensions=[

# Specify the RDS server based on the DB Instance name
        {
            'Name' : 'DBInstanceIdentifier',
            'Value' : 'dmansfieldlab2'

        }

    ],
)


for output in dbs['DBInstances']:
    print('DB Name: ' + output['DBName'] +
    '\nDB Software: ' + output['Engine'])

for output in cloudwatch_cpu['Datapoints']:
    print('\nMaximum CPU %: ' + str(output['Maximum']))
    print('Timestamp: ' + str(output['Timestamp']))


for output in cloudwatch_read_latency['Datapoints']:
    if output['Maximum'] > 10.0:
        print ('\nRead Latency: ' + str(output['Maximum']) + ' [WARNING]')
        print('Timestamp: ' + str(output['Timestamp']))

    else:
        print('\nRead Latency: ' + str(output['Maximum']))
        print('Timestamp: ' + str(output['Timestamp']))

for output in cloudwatch_write_latency['Datapoints']:
    if output['Maximum'] > 10.0:
        print ('\nWrite Latency: ' + str(output['Maximum']) + ' [WARNING]')
        print('Timestamp: ' + str(output['Timestamp']))

    else:
        print('\nWrite Latency: ' + str(output['Maximum']))
        print('Timestamp: ' + str(output['Timestamp']))
