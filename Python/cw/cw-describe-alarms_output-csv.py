import json
import boto3
import csv

client = boto3.client('cloudwatch')

row = 1

paginator = client.get_paginator('describe_alarms')
response_iterator = paginator.paginate()
# response_iterator = paginator.paginate(AlarmNames=['irvcoggwt02-CPU-Utilization', 'i-ffb08b38-AwOr-PdTibEms02-xvda1-LinuxDiskFreeSpace', 'AWOR-DVQDAAPP01-CPU-Utilization', 'AWOR-DVQLKAPP01-CPU-Utilization', 'AWOR-DVQMSDB01-CPU-Utilization', 'AWOR-DVSHGAPP01-CPU-Utilization', 'AWOR-DVSHGAPP02-CPU-Utilization'])
for page in response_iterator:
    alarm_list = []
    alarms = page['MetricAlarms']
    for alarm in alarms:
        alarm_list.append(alarm['AlarmName'])
    # for al in alarm_list:
    #     print(al)

# print(alarm_list)

    cpu_alarm = [x for x in alarm_list if '-StatusCheckFailed' in x]
    # print(cpu_alarm)

    for cpu in cpu_alarm:
        # with open('alarm_list_cpu.csv', 'w', newline='') as csvfile:
        #     writer = csv.writer(csvfile)
        #     writer.writerow(cpu_alarm)
            print(cpu)