import csv
import boto3
from collections import defaultdict

instance_list = []
region = 'us-west-2'

ec2client = boto3.client('ec2', region_name=region)


with open('instances.csv', 'r') as f:
    reader = csv.reader(f)
    instance_names = list(reader)

for instance_id in instance_names:   
    for i in instance_id:
        print(i)

for instances in instance_names:
    for instance in instances:
        responses = ec2client.describe_instances(
            Filters=[
                {
                    'Name': 'instance-id',
                    'Values': [
                        instance,
                    ]
                },
            ]
        )
        print(responses)

        # for reservations in responses['Reservations']:
        #     for instances in reservations['Instances']:
        #         for tags in instances['Tags']:
        #             if tags['Key'] == 'Name':
        #                 print(tags['Value'])
        #         # for instance_id in instances['']

        # for status in responses['Reservations']:
        #     for instances in status['Instances']:
        #         print(instances['InstanceId'])

        # for status in responses['Reservations']:
        #     for instances in status['Instances']:
        #        print(instances['State'])