#!/usr/binv/env python3
import functools
import os
import csv
import boto3



def ec2_describe_instances(region, instance_list):
    client = boto3.client('ec2', region_name=region)
    paginator = client.get_paginator('describe_instances')
    page = paginator.paginate(
        Filters=[
            {
                'Name': 'tag:Environment',
                'Values': [
                    'Production',
                ]
            },
        ],
        PaginationConfig={'PageSize': 1000}
    )
    for response in page:
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                instance_list.add(instance['InstanceId'])



def main():
    region = 'us-west-2'
    instance_list = set()
    ec2_describe_instances(region, instance_list)


    filename = '{}-prod-instances.csv'.format(region)


    # Write the list of ssm unmanaged servers to csvfile
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(instance_list)



if __name__ == '__main__':
    main()