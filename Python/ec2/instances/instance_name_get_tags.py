#!/usr/binv/env python3
import functools
import os
import csv
import boto3

@functools.lru_cache()
def boto3_client(resource, region=os.environ['AWS_DEFAULT_REGION']):
    """Create Boto3 Client from resource and region."""
    return boto3.client(resource, region)


def list_to_dict(obj, key='Key', value='Value'):
    return {e[key]: e[value] for e in obj}

def read_instance_names_from_file(filename='server_hostnames.csv'):
    with open(filename, newline='') as csvfile:
        return [r for r in csv.DictReader(csvfile)]

def describe_instances(**kwargs):
    for page in boto3_client('ec2').get_paginator('describe_instances').paginate(**kwargs):
        for reservation in page['Reservations']:
            for instance in reservation['Instances']:
                instance['Tags'] = list_to_dict(instance['Tags'])
                yield instance


def get_instance_names(instance_names):
    return describe_instances(Filters=[{'Name': 'tag:Name', 'Values':  instance_names}])




# def region_instance_names(data, region='Oregon', key='Instance Name'):
#     for row in data:
#         if row['Region'] == region:
#             yield row[key]

# def get_environment_tag(environment_tag):
#     for instance in get_instance_names(instance_names):
#         print(instance)
#         for reservation in page['Reservations']:
#             for instance in reservation['Instances']:
#                 instance['Tags'] = list_to_dict(instance['Tags'])
#     return instance



def main():

    # environment_tag = []
    instance_names = []
    instance = get_instance_names(instance_names)
    for i in instance:
        print(i)
        instance_names.append(i)

    print(instance_names)


    # instance_id = []
    # instance_name_to_id(instance_names)
    # instance = instance_name_to_id(instance_names)

    # instance_id_list(instance_id)
    # instances = instance_id_list(instance_id)

    # for i in instances:
    #     print(i)

if __name__ == '__main__':
    main()