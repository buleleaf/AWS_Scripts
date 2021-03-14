import boto3
import pprint
import csv

def get_instance_list(instance_list, instances):
    with open('instances.csv', 'r') as f:
        reader = csv.reader(f)
        instances = list(reader)
        # instance_list.append(instances)
        return instances


def main():
    instance_list = []
    region = 'us-west-2'
    get_instance_list(instance_list, instances)
    # ec2client = boto3.client('ec2', region_name=region)
    # for instance in instances:
    #     for i in instance:
    #         ec2client.describe_instances(
    #             Filters=[
    #                 {
    #                     'Name': 'instance-id',
    #                     'Values': instances,
    #                 },
    #             ]
    #         )

    print(instances)
# server_name = []

# for reservations in responses['Reservations']:
#     for instances in reservations['Instances']:
#         for tags in instances['Tags']:
#             if tags['Key'] == 'Name':
#                 print(tags['Value'])


#             if (instances['Value']):
#                 server_name.append(instances['Value'])
#                 server_name.append(instances['Key'])
# print(reservations)

# ec2 = boto3.client('ec2', region_name=region)

# responses = ec2.describe_instances(
#     Filters=[
#         {
#             'Name': 'platform',
#             'Values': [
#                 'windows',
#             ]
#         },
#     ],
# )
# instances = []
# for reservations in responses['Reservations']:
#     for instance in reservations['Instances']:
#         if (instance['InstanceId']):
#             instances.append(instance['InstanceId'])

# # print(instances)

# print(responses)