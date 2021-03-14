import csv
import boto3
from collections import defaultdict
import time

instance_list = []
region = 'us-west-2'

ec2 = boto3.resource('ec2', region_name=region)


with open('instances.csv', 'r') as f:
    reader = csv.reader(f)
    instance_id = list(reader)


for instances in instance_id:
    for instance in instances:
        ec2.Instance(instance).modify_attribute(
        DisableApiTermination={
            'Value': False
        })


        # # Get information for all stopped instances
        # stopped_instances = ec2.instances.filter(Filters=[{
        #     'Name': 'instance-state-name',
        #     'Values': ['stopped']}])

        # ec2info = defaultdict()
        # for instance in stopped_instances:
        #     for tag in instance.tags:
        #         if 'Name'in tag['Key']:
        #             name = tag['Value']
        #     # Add instance info to a dictionary         
        #     ec2info[instance.id] = {
        #         'Name': name,
        #         'ID': instance.id,
        #         # 'Type': instance.instance_type,
        #         'State': instance.state['Name'],
        #         # 'Private IP': instance.private_ip_address,
        #         # 'Launch Time': instance.launch_time
        #         }

        # attributes = ['Name', 'ID', 'State']
        # for instance_id, instance in ec2info.items():
        #     for key in attributes:
        #         print("{0}: {1}".format(key, instance[key]))
        #         print("------")

