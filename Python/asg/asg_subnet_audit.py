import boto3
import os
import functools
import pprint
os.environ['AWS_DEFAULT_REGION'] = 'us-west-2'

@functools.lru_cache()
def boto3_client(resource, region=os.environ['AWS_DEFAULT_REGION']):
    """Create Boto3 Client from resource and region."""
    return boto3.client(resource, region)

def describe_asg(**kwargs):
    for page in boto3_client('autoscaling').get_paginator('describe_auto_scaling_groups').paginate(**kwargs):
        for asg in page['AutoScalingGroups']:
            yield asg

def asg_info(subnets_1, subnets_2):
    asgs = describe_asg()
    for asg in asgs:
        subnet_list = asg['VPCZoneIdentifier'].split(",")
        if len(subnet_list) < 2:
            print(f"**WARNING** Auto Scaling Group: {asg['AutoScalingGroupName']} has ONLY 1 subnet")
            subnets_1[asg['AutoScalingGroupName']] = asg['VPCZoneIdentifier']
        else:
            print(f"Auto Scaling Group: {asg['AutoScalingGroupName']} has {len(subnet_list)} subnets")
            subnets_2[asg['AutoScalingGroupName']] = asg['VPCZoneIdentifier']


def main():
    subnets_1 = {}
    subnets_2 = {}
    asg_info(subnets_1, subnets_2)
    # asgs = describe_asg()
    # for asg in asgs:
    #     subnet_list = asg['VPCZoneIdentifier'].split(",")
    #     if len(subnet_list) < 2:
    #         print(f"**WARNING** Auto Scaling Group: {asg['AutoScalingGroupName']} has ONLY 1 subnet")
    #         subnets_1[asg['AutoScalingGroupName']] = asg['VPCZoneIdentifier']
    #     else:
    #         print(f"Auto Scaling Group: {asg['AutoScalingGroupName']} has {len(subnet_list)} subnets")
    #         subnets_2[asg['AutoScalingGroupName']] = asg['VPCZoneIdentifier']
    print(subnets_1)
    print(subnets_2)
# def get_asg_information():
#     asg_output = describe_asg()



    # def describe_asg_name():
#     asg_output = describe_asg()
#     return [a['AutoScalingGroupName'] for a in asg_output]

# def get_asg_subnet_count():
#     subnet_output = describe_asg()
#     return [a['VPCZoneIdentifier'] for a in subnet_output]

# def main():
    # asg_info = get_asg_information()
    # print(asg_info)

    # subnets = asg_subnet_count()
    # for s in subnets:
    #     print(s)
    # describe_asg_name()
    # asg_name = describe_asg_name()
    # print(asg_name)

    # subnet = get_asg_subnet_count()
    # print(subnet)
    # print(len(subnet))

if __name__ == '__main__':
    main()