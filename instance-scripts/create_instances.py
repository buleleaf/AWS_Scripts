import boto3
import time
from collections import defaultdict

# region = 'us-west-1'
# ami = 'ami-011b6930a81cd6aaf'

region_oregon = 'us-west-2'
ami_oregon = 'ami-01bbe152bf19d0289'
subnet_oregon = 'subnet-0a8f2683bf0b6ce80'
keyname_oregon = 'oregon'

region_virginia = 'us-east-1'
ami_virginia = 'ami-0c6b1d09930fac512'
subnet_virginia = 'subnet-030f50401cb8ad57e'
keyname_virginia = 'virginia'

region_ohio = 'us-east-2'
ami_ohio = 'ami-0cd3dfa4e37921605'
subnet_ohio = 'subnet-3b88ac53'

# Security Groups
# DMZ_Web_Work = 'sg-0e26ab317bf593eab'
# test = 'sg-06964326cadeb6071'

ec2 = boto3.resource('ec2', region_name=region_virginia)


instance = ec2.create_instances(
    ImageId=ami_virginia,
    MinCount=2,
    MaxCount=2,
    InstanceType='t2.micro',
    KeyName=keyname_virginia,
    # SecurityGroupIds=[DMZ_Web_Work],
    NetworkInterfaces=[
        {
            'AssociatePublicIpAddress': True,
            'DeviceIndex': 0,
            'SubnetId': subnet_virginia
        }
    ]
        )

time.sleep(5)

instance_status = ec2.instances.filter(Filters=[{
    'Name': 'instance-state-name',
    'Values': ['pending']}])


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
        print("{0}: {1}".format(key, instance[key]))
    print("-------------------------")
