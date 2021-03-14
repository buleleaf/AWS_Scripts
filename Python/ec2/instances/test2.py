import csv
import boto3
from collections import defaultdict
import time

instance_list = []
region = 'us-west-2'

ec2 = boto3.resource('ec2', region_name=region)


with open('delete-instances.csv', 'r') as f:
    reader = csv.reader(f)
    instance_id = list(reader)


for instances in instance_id:
    for instance in instances:
        #Terminate Instances
        ec2.instances.filter(InstanceIds=instances).terminate()

time.sleep(2)

# Get information for all terminating instances
terminated_instances = ec2.instances.filter(Filters=[{
    'Name': 'instance-state-name',
    'Values': ['terminated', 'terminating']}])

ec2info = defaultdict()
for instance in terminated_instances:
    for tag in instance.tags:
        if 'Name'in tag['Key']:
            name = tag['Value']
    # Add instance info to a dictionary         
    ec2info[instance.id] = {
        'Name': name,
        'ID': instance.id,
        # 'Type': instance.instance_type,
        'State': instance.state['Name'],
        # 'Private IP': instance.private_ip_address,
        # 'Launch Time': instance.launch_time
        }

attributes = ['Name', 'ID', 'State']
for instance_id, instance in ec2info.items():
    for key in attributes:
        print("{0}: {1}".format(key, instance[key]))
        print("------")




        # responses = ec2client.describe_instances(
        #     Filters=[
        #         {
        #             'Name': 'instance-id',
        #             'Values': [
        #                 instance,
        #             ]
        #         },
        #     ]
        # )


        # for reservations in responses['Reservations']:
        #     for instances in reservations['Instances']:
        #         for tags in instances['Tags']:
        #             if tags['Key'] == 'Name':
        #                 print(tags['Value'])
        #         for instance_id in instances['']

        # for status in responses['Reservations']:
        #     for instances in status['Instances']:
        #         print(instances['InstanceId'])

        # for status in responses['Reservations']:
        #     for instances in status['Instances']:
        #        print(instances['State'])