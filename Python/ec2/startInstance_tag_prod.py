"""
#  By: David Mansfield
#  Version: 1.0.1

This script will stop instances running based on Tag Value: Env=prod
"""

import boto3


# Connect to EC2
ec2 = boto3.resource('ec2')

# Get information for all running instances
instances = ec2.instances.filter(
    Filters=[{'Name': 'instance-state-name', 'Values': ['stopped']},{

# Instance information based on tag. To modify Tag Value, change the ['Env=  '] after 'Values':
    'Name': 'tag:Name', 'Values': ['Env=prod']

    }])

for instance in instances:
    for tags in instance.tags:
        if tags['Key'] == 'Name':
            name = tags['Value']

    print ('Starting instance Tagged:' + name + ' (' + instance.id + ')')
    instance.start()
