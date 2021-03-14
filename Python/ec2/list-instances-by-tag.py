"""
#  By: David Mansfield
#  Version: 1.0.1

This script will retreive all running instances and their state.
"""

from collections import defaultdict
import boto3

#  Change to the value to the desired region.
region = 'us-east-1'

ec2 = boto3.resource('ec2', region_name=region)


# Get information for all instances and state.
running_instances = ec2.instances.filter(Filters=[{
    'Name': 'instance-state-name',
    'Values': ['pending', 'running', 'stopping', 'stopped', 'terminated']}])

ec2info = defaultdict()
for instance in running_instances:
    for tag in instance.tags:
        if 'Name'in tag['Key']:
            name = tag['Value']
    # Add instance info to a dictionary
    ec2info[instance.id] = {
        'Tag': name,
        'Type': instance.instance_type,
        'State': instance.state['Name'],
        'Private IP': instance.private_ip_address,
        'Public IP': instance.public_ip_address,
        'Launch Time': instance.launch_time
        }

attributes = ['Tag', 'Type', 'Private IP', 'Public IP', 'Launch Time', 'State']
for instance_id, instance in ec2info.items():
    for key in attributes:
        print("{0}: {1}".format(key, instance[key]))
    print("-------------------------")
