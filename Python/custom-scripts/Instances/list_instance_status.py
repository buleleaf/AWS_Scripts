from collections import defaultdict
import threading
import boto3
import time
import csv

"""
A tool for retrieving basic information from the running EC2 instances.
"""
with open('instances.csv', 'r') as f:
    reader = csv.reader(f)
    instances = list(reader)

# Connect to EC2
ec2 = boto3.resource('ec2')

# running_instances = ec2.instances.filter(
#         Filters=[
#         {
#             'Name': 'tag:Name',
#             'Values': [
#                 instances,
#             ]
#         },
#     ]
# )

# # Get information for all running instances
instance_status = ec2.instances.filter(Filters=[{
    'Name': 'instance-state-name',
    'Values': ['running']}])


ec2info = defaultdict()
for instance in instance_status:
    ec2info[instance.id] = {
        'Type': instance.instance_type,
        'ID': instance.id,
        'Private IP': instance.private_ip_address,
        'State': instance.state['Name'],
        }

attributes = ['Type', 'ID', 'Private IP', 'State']
for instance_id, instance in ec2info.items():
    for key in attributes:
        print(instance[key])
    #     print("{0}: {1}".format(key, instance[key]))
    # print("-------------------------")