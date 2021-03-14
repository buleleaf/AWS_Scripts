#!/usr/binv/env python3
import functools
import os
import csv
import boto3
import json

# region = 'us-west-2'
# client = boto3.client('ssm', region_name=region)
# resp = client.describe_instance_information()

# print(resp)
# def ssm_instance_json(ssm_list):
#     with open('ssm_instances.json') as f:
#         data = json.load(f)
#     for instanceinfo in data['InstanceInformationList']:
#         ssm_list.add(instanceinfo['InstanceId'])
#     return instanceinfo


    # for instance in instanceinfo['InstanceId']:
    #     print(instance)


# for instanceinfo in resp['InstanceInformationList']:
#     print(instanceinfo['InstanceId'])

# print(resp)

# This only find the instace ID's and is not complete


def read_instance_names_from_file(filename='asadmin_instances_missing_metrics.csv'):
    with open(filename, newline='') as csvfile:
        return [r for r in csv.reader(csvfile)]


# def get_ec2_instances(region):
#     instance_list = set()
#     ec2client = boto3.client('ec2', region_name=region)
#     resp = ec2client.describe_instances(Filters=[{'Name': 'tag:Name', 'Values':  instance_names}])
#     for servers in read_instance_names_from_file():
#         for reservation in resp['Reservations']:
#             for instance in reservation['Instances']:  
#                 instance_list.add(instance['InstanceId'])

def ec2_describe_instances(region, instances):
    print("Getting Instance Id's from CSV File")
    client = boto3.client('ec2', region_name=region)
    paginator = client.get_paginator('describe_instances')
    for servers in read_instance_names_from_file():
        for server in servers:
            page = paginator.paginate(
                Filters=[
                    {
                        'Name': 'tag:Name',
                        'Values': [
                            server,
                        ]
                    },
                ],
                PaginationConfig={'PageSize': 1000}
            )
            for response in page:
                for reservation in response['Reservations']:
                    for instance in reservation['Instances']:
                        instances.add(instance['InstanceId'])
    return instances

# def ssm_describe_instance_information(region, ssm_list):
    # print("Getting list of SSM servers")
    # ssm = set()
    # client = boto3.client('ssm', region_name=region)
    # resp = client.describe_instance_information()
    # for instance in resp:
    #     ssm_list.append(instance['InstanceId'])
    # return instance
    # return resp


# def ssm_describe_instance_information(region):
#     print("Getting list of SSM managed servers")
#     ssm = set()
#     client = boto3.client('ssm', region_name=region)
#     paginator = client.get_paginator('describe_instance_information')
#     page = paginator.paginate()
#     for response in page:
#         for instanceinfo in response['InstanceInformationList']:
#             if (instanceinfo['InstanceId']):
#                 ssm.add(instanceinfo['InstanceId'])
#     return ssm



def main():
    instances = set()
    region = 'us-west-2'
    # client = boto3.client('ssm', 'us-west-2')
    ec2_describe_instances(region, instances)
    # ssm_describe_instance_information(region)
    # managed_instances = ssm_describe_instance_information(region)
    # unmanaged_instances = managed_instances.difference(instances)
    # print("Getting list of Unmanaged servers")
    for i in instances:
        print(i)
    # print(unmanaged_instances)

    # print(ec2_instances)
    # for i in ec2_instances:
    #     print(i)

    # for i in ssm_instances:
    #     print(i)


# def main():
#     region = 'us-west-2'
#     ssm_list = set()
#     ssm_instance_json(ssm_list)
#     ec2_describe_instances(region)
#     instances = ec2_describe_instances(region)
#     unmanaged = instances.difference(ssm_list)
#     print(instances)


    # instance_list = set()
    # ssm_list = []
    # ec2_describe_instances(region, instance_list)
    # ssm_describe_instance_information(region, ssm_list)
    # print(instance_list)

    # print(ssm_list)

    # ssm_instances = ssm_describe_instance_information(region, ssm_list)
    # print("Running a diff on CSV Instances and the SSM Managed")
    # print(ssm_instances)
    # managed_instances = ssm_instances.difference(instance_list)
    # print(managed_instances)
    # for mi in managed_instances:
    #     print(mi)


if __name__ == '__main__':
    main()