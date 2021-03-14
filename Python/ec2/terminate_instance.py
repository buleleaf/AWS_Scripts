import time
from collections import defaultdict
import boto3
ec2 = boto3.resource('ec2')
ec2_filter = [{'Name': 'instance-state-name', 'Values': ['running']}]

ec2.instances.filter(Filters=ec2_filter).terminate()

time.sleep(5)

# Get information for all running instances
instance_status = ec2.instances.filter(Filters=[{
    'Name': 'instance-state-name',
    'Values': ['shutting-down']}])


ec2info = defaultdict()
for instance in instance_status:
    ec2info[instance.id] = {
        'Type': instance.instance_type,
        'ID': instance.id,
        'Private IP': instance.private_ip_address,
        'Public IP': instance.public_ip_address,
        'State': instance.state['Name'],
        }

attributes = ['Type', 'ID', 'Private IP', 'Public IP', 'State']
for instance_id, instance in ec2info.items():
    for key in attributes:
        print("{0}: {1}".format(key, instance[key]))
    print("-------------------------")

