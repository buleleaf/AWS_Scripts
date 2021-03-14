import time
import boto3
from collections import defaultdict

# region = 'us-east-1'
# ami = 'ami-04d29b6f966df1537'

region = 'us-west-2'
ami = 'ami-0e34e7b9ca0ace12d'

ec2 = boto3.resource('ec2', region_name=region)


instance = ec2.create_instances(
    ImageId=ami,
    MinCount=1,
    MaxCount=1,
    KeyName='onica-test',
    InstanceType='t2.small',

    TagSpecifications=[
        {
            'ResourceType': 'instance',
            'Tags': [
                {
                    "Key": "Name",
                    "Value": "Test1"
                }
            ]
        },
        {
            'ResourceType': 'volume',
            'Tags': [
                {
                    "Key": "Name",
                    "Value": "Test1"
                }
            ]
        }
    ]
)

time.sleep(2)

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