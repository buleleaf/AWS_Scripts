
import boto3
import datetime


region = 'us-east-1'

rds = boto3.client('rds', region_name=region)

dbs = rds.describe_db_instances()

cloudwatch = boto3.client('cloudwatch', region_name=region)

cloudwatch_cpu = cloudwatch.get_metric_statistics(
    Namespace='AWS/RDS',
    MetricName='CPUUtilization',
    # StartTime=datetime.datetime(2018, 9, 24, 23, 40),
    # EndTime=datetime.datetime(2018, 9, 24, 23, 45),
    StartTime=datetime.datetime.utcnow() - datetime.timedelta(seconds=60),
    EndTime=datetime.datetime.utcnow(),
    Statistics=['Maximum'],
    Period=300,
    Dimensions=[],
)

cloudwatch_read_latency = cloudwatch.get_metric_statistics(
    Namespace='AWS/RDS',
    MetricName='ReadLatency',
    StartTime=datetime.datetime(2018, 9, 24, 23, 40),
    EndTime=datetime.datetime(2018, 9, 24, 23, 45),
    # StartTime=datetime.datetime.utcnow() - datetime.timedelta(seconds=60),
    # EndTime=datetime.datetime.utcnow(),
    Statistics=['Maximum'],
    Period=300,
    Dimensions=[],
)

cloudwatch_write_latency = cloudwatch.get_metric_statistics(
    Namespace='AWS/RDS',
    MetricName='WriteLatency',
    StartTime=datetime.datetime(2018, 9, 24, 23, 40),
    EndTime=datetime.datetime(2018, 9, 24, 23, 45),
    # StartTime=datetime.datetime.utcnow() - datetime.timedelta(seconds=60),
    # EndTime=datetime.datetime.utcnow(),
    Statistics=['Maximum'],
    Period=300,
    Dimensions=[],
)

#
# for kv in cloudwatch_stats.values():
#     print(kv)

# pprint(cloudwatch_stats)
#

for output in dbs['DBInstances']:
    print('DB Name: ' + output['DBName'] +
    '\nDB Software: ' + output['Engine'])

for output in cloudwatch_cpu['Datapoints']:
    print('\nMaximum CPU %: ' + str(output['Maximum']))
    print('Timestamp: ' + str(output['Timestamp']))


for output in cloudwatch_read_latency['Datapoints']:
    if output['Maximum'] > 1.0:
        print ('\nRead Latency: ' + str(output['Maximum']) + ' [WARNING]')
        print('Timestamp: ' + str(output['Timestamp']))

    else:
        print('\nRead Latency: ' + str(output['Maximum']))
        print('Timestamp: ' + str(output['Timestamp']))

for output in cloudwatch_write_latency['Datapoints']:
    if output['Maximum'] > 1.0:
        print ('\nWrite Latency: ' + str(output['Maximum']) + ' [WARNING]')
        print('Timestamp: ' + str(output['Timestamp']))

    else:
        print('\nWrite Latency: ' + str(output['Maximum']))
        print('Timestamp: ' + str(output['Timestamp']))




    # print('\nCPU: ' + str(output['Maximum']))
    # print('Timestamp: ' + str(output['Timestamp']))

    # for warning in str(output['Maximum']):
    #     print warning,
    #
    #     if warning == 2.00000000000:
    #         print ('\nCPU: ' + str(output['Maximum']) + ' [WARNING]')
    #         print('Timestamp: ' + str(output['Timestamp']))
    #
    #     else:
    #         print('\nCPU: ' + str(output['Maximum']))
    #         print('Timestamp: ' + str(output['Timestamp']))



    # print('\nCPU %: ' + str(output['Maximum']))

    # print('Timestamp: ' + str(output['Timestamp']))

# for output in cloudwatch_latency['Datapoints']:
#     for value in str(output['Maximum']):
#         if value > 0.0:
#             print ('\nLatency: ' + str(output['Maximum']) + ' [WARNING]')
#         else:
#             print('\nLatency: ' + str(output['Maximum']))
#
#     print('Timestamp: ' + str(output['Timestamp']))



# for output in cloudwatch_stats['Datapoints']:
#     print('\nTimestamp: ' + str(output['Timestamp']))
#     print('Maximum CPU %: ' + str(output['Maximum']))


# aws cloudwatch get-metric-statistics
#
# --region--namespace 'AWS/RDS'
# --metric-name 'CPUUtilization'
# --start-time '2018-09-24T21:34:00Z'
# --end-time '2018-09-24T21:52:00Z'
# --period 60
# --statistics 'Maximum'
