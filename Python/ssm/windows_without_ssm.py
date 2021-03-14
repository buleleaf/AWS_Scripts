import boto3
import json


def get_ec2_instances(region):
    instances = set()
    ec2client = boto3.client('ec2', region_name=region)
    responses = ec2client.describe_instances(
        # Filters=[
        #     {
        #         'Name': 'platform',
        #         'Values': [
        #             'windows',
        #         ]
        #     },
        # ],
    )
    for reservations in responses['Reservations']:
        for instance in reservations['Instances']:
            if (instance['InstanceId']):
                instances.add(instance['InstanceId'])
    print(len(instances))
    return instances

def get_ssm_instances(region, ssm):
    paginator = boto3.client('ssm').get_paginator('describe_instance_information')
    page = paginator.paginate()
    for response in page:
        for instanceinfo in response['InstanceInformationList']:
            ssm.add(instanceinfo['InstanceId'])
    print("Instances in SSM = ")
    print(len(ssm))



def main():
    region = 'us-west-2'
    ssm = set()

    get_ssm_instances(region, ssm)
    instances = get_ec2_instances(region)
    not_in_ssm = instances.difference(ssm)
    for instance in not_in_ssm:
        print(instance)

if __name__ == '__main__':
    main()