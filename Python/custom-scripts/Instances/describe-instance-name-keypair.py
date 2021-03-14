import boto3
import pprint
import csv

region = 'eu-central-1'
ec2client = boto3.client('ec2', region_name=region)
with open('instances.csv', 'r') as f:
    reader = csv.reader(f)
    instances = list(reader)


# print(instances)

instance_list = []

for instance in instances:
    for i in instance:
        instance_list.append(i)

response = ec2client.describe_instances(
    Filters=[
        {
            'Name': 'key-name',
            'Values': [
                'Onica-ELS-Frankfurt'
            ]
        }
    ]
)



# server_name = []

for reservations in response['Reservations']:
    for instances in reservations['Instances']:
        for tags in instances['Tags']:
            if tags['Key'] == 'Name':
                print(tags['Value'])
        print(instances['InstanceId'])
        # try:
        #     print(instances['KeyName'])
        # except:
        #     pass
        # print("\n")


#             if (instances['Value']):
#                 server_name.append(instances['Value'])
#                 server_name.append(instances['Key'])
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