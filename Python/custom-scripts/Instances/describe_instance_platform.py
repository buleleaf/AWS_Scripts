import boto3
from botocore.exceptions import ClientError
import csv



# with open('instances.csv', 'r') as f:
#     csv_reader = csv.reader(f)
#     instances = list(csv_reader)


ec2client = boto3.client('ec2', region_name='us-west-2')
responses = ec2client.describe_instances(
    InstanceIds=['i-d7ae7d43']
)
instance_result = set()
for reservations in responses['Reservations']:
    for instance in reservations['Instances']:
        if (instance['InstanceId']):
            instance_result.add(instance['InstanceId'])
print(len(instance_result))
print(instance_result)
print(responses)


# try:
#     response = ec2.delete_security_group(GroupId='{}'.format(security_groups))
#     print(response)
#     .format(str(security_groups)[-1:1]))
#     print('Deleting Security Group: {}'.format(str(security_groups)[-1:1]))
#     print('Security Group Deleted')
# except ClientError as e:
#     print(e)    
#     for sg in security_groups:
#         print(sg)
#         response = ec2.delete_security_group(GroupId='sg-0683d3523a393f9e1')
        
#         # try:
#             for gid in sg_groupid:
#                 response = ec2.delete_security_group(GroupId='{}'.format(gid))
#                 print('Security Group Deleted')
#         except ClientError as e:
#             print(e)
