import boto3
from botocore.exceptions import ClientError
import csv

# Create EC2 client
ec2 = boto3.client('ec2')


with open('sg.csv', 'r') as f:
    csv_reader = csv.reader(f)
    security_groups = list(csv_reader)

# Delete security group
try:
    response = ec2.delete_security_group(GroupId='{}'.format(security_groups))
    print(response)
    # # .format(str(security_groups)[-1:1]))
    # print('Deleting Security Group: {}'.format(str(security_groups)[-1:1]))
    # print('Security Group Deleted')
except ClientError as e:
    print(e)    
    # for sg in security_groups:
    #     print(sg)
    #     response = ec2.delete_security_group(GroupId='sg-0683d3523a393f9e1')
        
    #     # try:
        #     for gid in sg_groupid:
        #         response = ec2.delete_security_group(GroupId='{}'.format(gid))
        #         print('Security Group Deleted')
        # except ClientError as e:
        #     print(e)
