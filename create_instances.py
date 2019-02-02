import time
import boto3
from collections import defaultdict

region = 'us-west-1'
ami = 'ami-011b6930a81cd6aaf'

# region = 'us-west-2'
# ami = 'ami-01bbe152bf19d0289'

ec2 = boto3.resource('ec2', region_name=region)


instance = ec2.create_instances(
    ImageId=ami,
    MinCount=2,
    MaxCount=2,
    SecurityGroupIds=['sg-04eff5e1d0302a411'],
    KeyName='work-norcal',
    InstanceType='t2.micro'
    )

time.sleep(5)

# Get information for all running instances
instance_status = ec2.instances.filter(Filters=[{
    'Name': 'instance-state-name',
    'Values': ['pending']}])


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
