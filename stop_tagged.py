import boto3
from collections import defaultdict

# Connect to EC2
ec2 = boto3.resource('ec2')

# Get information for all running instances
instances = ec2.instances.filter(
    Filters=[{'Name': 'instance-state-name', 'Values': ['running']},{

#  To stop instance based on the tag, change the ['   '] after 'Values':
    'Name': 'tag:Name', 'Values': ['Prod']

    }])

for instance in instances:
    for tags in instance.tags:
        if tags['Key'] == 'Name':
            name = tags['Value']

    print ('Stopping instance Tagged:' + name + ' (' + instance.id + ')')
    instance.stop()
