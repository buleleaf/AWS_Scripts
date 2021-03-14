import random
import string
import boto3
import time
from collections import defaultdict

client = boto3.client('rds', region_name='us-west-2')

response = client.describe_db_instances()

instance_list = []
for instances in response['DBInstances']:
    if (instances['DBInstanceIdentifier']):
        instance_list.append(instances['DBInstanceIdentifier'])

print(instance_list)

encrypted_list = []
for encryption in response['DBInstances']:
    encrypted = encryption['StorageEncrypted']
    
    for result in encrypted:
        encrypted_list.append(result)

print(encrypted_list)
# instance_result = set()
# for reservations in responses['Reservations']:
#     for instance in reservations['Instances']:
#         if (instance['InstanceId']):
#             instance_result.add(instance['InstanceId'])
# print(len(instance_result))
# print(instance_result)


# instance_result = set()
# for reservations in responses['Reservations']:
#     for instance in reservations['Instances']:
#         if (instance['InstanceId']):
#             instance_result.add(instance['InstanceId'])
# print(len(instance_result))
# print(instance)