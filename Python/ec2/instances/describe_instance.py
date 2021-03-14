import boto3
import pprint
import os
import pprint

REGION = os.getenv('AWS_REGION', 'us-west-2')

def convert_list_to_dict(obj, key='Key', value='Value'):
    return {e[key]: e[value] for e in obj}


def describe_all_instances(client):
    instances = []
    paginator = client.get_paginator('describe_instances')
    response = paginator.paginate()
    for page in response:
        for reservations in page['Reservations']:
            for instance in reservations['Instances']:
                instance['Tags'] = convert_list_to_dict(instance['Tags'])
                instances.append(instance)
    pprint.pprint(instances)
    return instances

def main():
    client = boto3.client('cloudwatch', REGION)
    ec2_client = boto3.client('ec2', REGION)
    instances = describe_all_instances(ec2_client)
    # print(instances)s

if __name__ == '__main__':
    main()

# responses = ec2client.describe_instances(
#     Filters=[
#         {
#             'Name': 'image-id',
#             'Values': [
#                 'ami-f08b0388',
#             ]
#         },
#     ],
    # InstanceIds=[
    #     'i-0dd58e465f9ef8a1f'
    # ]
# )

# for reservations in responses['Reservations']:
#     for instances in reservations['Instances']:
#         for tags in instances['Tags']:
#             if tags['Key'] == 'Name':
#                 print(tags['Value'])

# print(responses)

#             if (instance['Value']):
#             ssm.add(instance['Value'])
#             ssm.add(instance['Key'])
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