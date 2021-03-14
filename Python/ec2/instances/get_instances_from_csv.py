from collections import defaultdict
import csv
import boto3

"""
A tool for retrieving basic information from the running EC2 instances.
"""

with open('server_hostnames.csv', 'r') as f:
    reader = csv.reader(f)
    hostnames = list(reader)

instance_list = []

for instance in hostnames:
    for i in instance:
        instance_list.append(i)
# Connect to EC2
ec2 = boto3.resource('ec2')

# Get information for all running instances
running_instances = ec2.instances.filter(Filters=[{
    'Name': 'tag:Name',
    'Values': instance_list}])

ec2info = defaultdict()
for instance in running_instances:
    for name in instance.tags:
        if 'Name'in name['Key']:
            name = name['Value']
    # for env in instance.tags:
    #     if 'Environment'in env['Key']:
    #         environment = env['Value']
    # for app in instance.tags:
    #     if 'Application'in app['Key']:
            # application = app['Value']
    # Add instance info to a dictionary
    ec2info[instance.id] = {
        'Name': name,
        # 'Environment': env,
        # 'Application': app,
        # 'Type': instance.instance_type,
        # 'State': instance.state['Name'],
        # 'Private IP': instance.private_ip_address,
        # 'Public IP': instance.public_ip_address,
        # 'Launch Time': instance.launch_time
        }

# attributes = ['Name', 'Environment', 'Application']
attributes = ['Name']
for instance_id, instance in ec2info.items():
    for key in attributes:
        print("{0}: {1}".format(key, instance[key]))
    print("------")