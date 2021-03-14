#!/usr/binv/env python3
import functools
import os
import csv
import boto3
""" WITHOUT USING FUNCTIONS """

client = boto3.client('ec2','us-west-2')

with open('server_hostnames.csv', 'r') as f:
    reader = csv.reader(f)
    hostnames = list(reader)

instance_list = []

for instance in hostnames:
    for i in instance:
        instance_list.append(i)

response = client.describe_instances(
    Filters=[
        {
            'Name': 'Tag:Name',
            'Values': instance_list
        },
    ]
)

print(response)
# print(instance_list)
# print(server)


""" USING FUNCTIONS """


# This works
# def read_instance_names_from_file(filename='instances-missing-metrics.csv'):
#     with open(filename, newline='') as csvfile:
#         return [r for r in csv.reader(csvfile)]
# def print_csv(servers):
#     for server in read_instance_names_from_file():
#         servers.append(server)

# def main():
#     servers = []
#     print_csv(servers)

#     print(servers)



# @functools.lru_cache()
# def boto3_client(resource, region=os.environ['AWS_DEFAULT_REGION']):
#     """Create Boto3 Client from resource and region."""
#     return boto3.client(resource, region)


# def read_instance_names_from_file(filename='server_hostnames.csv'):
#     with open(filename, newline='') as csvfile:
#         return [r for r in csv.reader(csvfile)]

# def list_to_dict(obj, key='Key', value='Value'):
#     return {e[key]: e[value] for e in obj}

# def ec2_describe_instances(region, instance_list):
#     client = boto3.client('ec2', region_name=region)
#     paginator = client.get_paginator('describe_instances')
#     for servers in read_instance_names_from_file():
#         for server in servers:
#             page = paginator.paginate(
#                 Filters=[
#                     {
#                         'Name': 'tag:Name',
#                         'Values': [
#                             server,
#                         ]
#                     },
#                 ],
#                 PaginationConfig={'PageSize': 1000}
#             )
#             for response in page:
#                 for reservation in response['Reservations']:
#                     for instance in reservation['Instances']:
#                         instance['Tags'] = list_to_dict(instance['Tags'])
#     yield instance_list

# def ssm_describe_instance_information(region):
#     ssm = set()
#     client = boto3.client('ssm', region_name=region)
#     resp = client.describe_instance_information()
#     for instanceinfo in resp['InstanceInformationList']:
#         for instance in instanceinfo['InstanceId']:
#             ssm.add(instance)
#     return ssm

# def read_instance_names_from_file(filename='instances-missing-metrics.csv'):
#     with open(filename, newline='') as csvfile:
#         return [r for r in csv.reader(csvfile)]

# # def print_csv(servers):
# #     for server in read_instance_names_from_file():
# #         servers.append(server)

# def list_to_dict(obj, key='Key', value='Value'):
#     return {e[key]: e[value] for e in obj}

# def describe_instances(**kwargs):
#     for page in boto3_client('ec2').get_paginator('describe_instances').paginate(**kwargs):
#         for reservation in page['Reservations']:
#             for instance in reservation['Instances']:
#                 instance['Tags'] = list_to_dict(instance['Tags'])
#                 yield instance

# def instance_name_to_id(instance_names):
#     return describe_instances(Filters=[{'Name': 'tag:Name', 'Values':  instance_names}])




# def main():
#     region = 'us-west-2'
#     instance_list = set()
#     ec2_describe_instances(region, instance_list)
    # ssm_instances = ssm_describe_instance_information(region)
    # managed_instances = ssm_instances.difference(instance_list)
    # for mi in managed_instances:
    #     print(mi)

    # print(instance_list)

    # print(instance_list)



# if __name__ == '__main__':
#     main()