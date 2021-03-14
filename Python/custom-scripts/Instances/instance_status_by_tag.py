from collections import defaultdict
import threading
import boto3
import time
import csv

"""
A tool for retrieving basic information from the running EC2 instances.
"""


def get_stopped_instances(ec2client, instances):
    stopped_instances = ec2client.describe_instances(
        Filters=[
            {
                'Name': 'tag:Name',
                'Values': [
                    instances,
                ]
            },
        ]
    )
    # print(stopped_instances)
    return(stopped_instances)

# # Get information for all running instances
# def get_instance_status(ec2, stopped_instances):
#     instance_status = ec2.instances.filter(Filters=[{
#         'Name': 'instance-state-name',
#         'Values': ['stopped']}])





def main():
    """Main."""
    region = 'us-west-2'
# Connect to EC2
    ec2client = boto3.client('ec2', region_name=region)

    instance_list = []

    with open('instances.csv', 'r') as f:
        reader = csv.reader(f)
        instances = list(reader)
        for i in instances:
            instance_list.append(i[2:-2])

    print(instance_list)

    stopped_instances = get_stopped_instances(ec2client, instances)

    print(stopped_instances)

    # for reservations in stopped_instances['Reservations']:
    #     for instances in reservations['Instances']:
    #         for tags in instances['Tags']:
    #             if tags['Key'] == 'Name':
    #                 print(tags['Value'])

    ec2info = defaultdict()
    for instance in instance_status:
        ec2info[instance.id] = {
            'Type': instance.instance_type,
            'ID': instance.id,
            'Private IP': instance.private_ip_address,
            'State': instance.state['Name'],
            }

    attributes = ['ID']
    for instance_id, instance in ec2info.items():
        for key in attributes:
            print(instance[key])
        #     print("{0}: {1}".format(key, instance[key]))
        # print("-------------------------")

if __name__ == '__main__':
    main()