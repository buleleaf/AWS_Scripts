import json
import boto3
import xlsxwriter

client = boto3.client('cloudwatch')

workbook = xlsxwriter.Workbook('alarm_list_cpu.xlsx')
worksheet = workbook.add_worksheet(name='alarm_list')
text_format = workbook.add_format({'text_wrap': True,'align':'vcenter'})
heading_format = workbook.add_format({'bold': True, 'font_color': 'red','align':'center'})
row = 2

worksheet.write('A1', 'Alarm Name',heading_format)

def write_to_excel(worksheet,alarm):
    worksheet.write('A'+str(row),alarm['AlarmName'],text_format)

paginator = client.get_paginator('describe_alarms')
response_iterator = paginator.paginate()
# response_iterator = paginator.paginate(AlarmNames=['irvcoggwt02-CPU-Utilization', 'i-ffb08b38-AwOr-PdTibEms02-xvda1-LinuxDiskFreeSpace', 'AWOR-DVQDAAPP01-CPU-Utilization', 'AWOR-DVQLKAPP01-CPU-Utilization', 'AWOR-DVQMSDB01-CPU-Utilization', 'AWOR-DVSHGAPP01-CPU-Utilization', 'AWOR-DVSHGAPP02-CPU-Utilization'])
for page in response_iterator:
    alarms = page['MetricAlarms']
    alarm_list = []
    for alarm in alarms:
        alarm_list.append(alarm['AlarmName'])
    cpu_alarm = [x for x in alarm_list if '-CPU-Utilization' in x]
    for cpu in cpu_alarm:
        write_to_excel(worksheet,alarm)
        row=row+1
        print(cpu)
        # print(alarm['AlarmName'])

workbook.close()