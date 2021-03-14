import boto3
from collections import defaultdict

# Connect to EC2
ec2 = boto3.resource('ec2')

# Get information for all running instances
instances = ec2.instances.filter(
    Filters=[{'Name': 'instance-state-name', 'Values': ['stopped']},{

# Instance information based on tag. To modify Tag Value, change the ['   '] after 'Values':
    'Name': 'tag:Name', 'Values': ['Prod']

    }])

for instance in instances:
    for tags in instance.tags:
        if tags['Key'] == 'Name':
            name = tags['Value']

    print ('Starting instance Tagged:' + name + ' (' + instance.id + ')')
    instance.start()
