import boto3

region = 'us-west-2'
# session = boto3.Session()

ec2 = boto3.client('ec2', region_name=region)
response = ec2.describe_key_pairs()['KeyPairs']

print(response)
# for key in response:
#     found_instance = ec2.describe_instances(
#         Filters=[
#             {
#                 'Name': 'key-name',
#                 'Values': [key['KeyName']]
#             }
#         ]
#     )['Reservations']
#     if len(found_instance) == 1:
#         print (key['KeyName'] + " is used")
#     elif len(found_instance) == 0:
#         print (key['KeyName'] + " is unused")