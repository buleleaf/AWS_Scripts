import boto3

client = boto3.client('ec2', region_name='us-west-2')

response = client.run_instances(
    BlockDeviceMappings=[
        {
            'DeviceName': '/dev/xvda',
            'Ebs': {

                'DeleteOnTermination': True,
                'VolumeSize': 8,
                'VolumeType': 'gp2'
            },
        },
    ],
    ImageId='ami-081c3775f479265ea',
    InstanceType='t2.nano',
    MaxCount=1,
    MinCount=1,
    Monitoring={
        'Enabled': False
    },
    SubnetId='subnet-2ebc6f05',
    SecurityGroupIds=[
        'sg-0996cc3c9ec337b74',
    ],
)

# response = client.run_instances(
#     BlockDeviceMappings=[
#         {
#             'DeviceName': '/dev/xvda',
#             'Ebs': {
#                 'VolumeSize': root_drive_size,
#                 'VolumeType': root_drive_type,
#                 'DeleteOnTermination': True,
#             },
#         },
#     ],
#     ImageId=ami_id,
#     InstanceType=instance_type,
#     KeyName=keyname,
#     MinCount=1,
#     MaxCount=1,
#     Monitoring={
#         'Enabled': False
#     },
#     SubnetId=subnet_id,
#     SecurityGroups=[
#         sg_1,
#     ],
    # IamInstanceProfile={
    #     'Arn': 'arn:aws:iam::590992000271:instance-profile/EdwardsEC2RoleforSSMandCWAgent'
    # },
    # NetworkInterfaces=[
    #     {
    #         'AssociatePublicIpAddress': False,
    #         'DeviceIndex': 0,
    #         'SubnetId': subnet_id,
    #         'Groups': [
    #             sg_1,
    #             # sg_2,
    #             # sg_3,
    #         ]
    #     }
    # ],
    # TagSpecifications=[
    #     {
    #         'ResourceType': 'instance',
    #         'Tags': [
    #             {
    #                 "Key": "Application",
    #                 "Value": "Patch-Testing"
    #             },
    #             {
    #                 "Key": "ApplicationTier",
    #                 "Value": "Application"
    #             },
    #             {
    #                 "Key": "Managed",
    #                 "Value": "Yes"
    #             },
    #             {
    #                 "Key": "Environment",
    #                 "Value": "Development"
    #             },
    #             {
    #                 "Key": "Name",
    #                 "Value": "els-patch-test-non-prod"
    #             },
    #             {
    #                 "Key": "TakeNightlySnapshot",
    #                 "Value": "No"
    #             },
    #             {
    #                 "Key": "FileBackup",
    #                 "Value": "No"
    #             },
    #             {
    #                 "Key": "RequestNumber",
    #                 "Value": "N/A"
    #             },
    #             {
    #                 "Key": "ReviewDate",
    #                 "Value": "N/A"
    #             },
    #             {
    #                 "Key": "CostCenter",
    #                 "Value": "0000000000"
    #             },
    #             {
    #                 "Key": "ServiceOwner",
    #                 "Value": "onica"
    #             },
    #             {
    #                 "Key": "TechnicalOwner",
    #                 "Value": "onica"
    #             },
    #             {
    #                 "Key": "ContactPreference",
    #                 "Value": "Email"
    #             },
    #             {
    #                 "Key": "PatchGroup",
    #                 "Value": "PilotManualReboot"
    #             },
    #             {
    #                 "Key": "Schedule",
    #                 "Value": "AlwaysOn"
    #             },
    #             {
    #                 "Key": "Purpose",
    #                 "Value": "Integration"
    #             },
    #             {
    #                 "Key": "Validated",
    #                 "Value": "Yes"
    #             }
    #         ]
    #     },
#         {
#             'ResourceType': 'volume',
#             'Tags': [
#                 {
#                     "Key": "Application",
#                     "Value": "Patch-Testing"
#                 },
#                 {
#                     "Key": "ApplicationTier",
#                     "Value": "Application"
#                 },
#                 {
#                     "Key": "Managed",
#                     "Value": "Yes"
#                 },
#                 {
#                     "Key": "Environment",
#                     "Value": "Development"
#                 },
#                 {
#                     "Key": "Name",
#                     "Value": "els-patch-test-non-prod"
#                 },
#                 {
#                     "Key": "TakeNightlySnapshot",
#                     "Value": "No"
#                 },
#                 {
#                     "Key": "FileBackup",
#                     "Value": "No"
#                 },
#                 {
#                     "Key": "RequestNumber",
#                     "Value": "N/A"
#                 },
#                 {
#                     "Key": "ReviewDate",
#                     "Value": "N/A"
#                 },
#                 {
#                     "Key": "CostCenter",
#                     "Value": "0000000000"
#                 },
#                 {
#                     "Key": "ServiceOwner",
#                     "Value": "onica"
#                 },
#                 {
#                     "Key": "TechnicalOwner",
#                     "Value": "onica"
#                 },
#                 {
#                     "Key": "ContactPreference",
#                     "Value": "Email"
#                 },
#                 {
#                     "Key": "PatchGroup",
#                     "Value": "PilotManualReboot"
#                 },
#                 {
#                     "Key": "Schedule",
#                     "Value": "AlwaysOn"
#                 },
#                 {
#                     "Key": "Purpose",
#                     "Value": "Integration"
#                 },
#                 {
#                     "Key": "Validated",
#                     "Value": "Yes"
        #         }
        #     ]
        # }
    # ]
# )

# time.sleep(5)

# instance_status = client.instances.filter(Filters=[{
#     'Name': 'instance-state-name',
#     'Values': ['pending']}])


# ec2info = defaultdict()
# for instance in instance_status:
#     ec2info[instance.id] = {
#         'Type': instance.instance_type,
#         'ID': instance.id,
#         'Private IP': instance.private_ip_address,
#         'State': instance.state['Name'],
#         }

# attributes = ['Type', 'ID', 'Private IP', 'State']
# for instance_id, instance in ec2info.items():
#     for key in attributes:
#         print("{0}: {1}".format(key, instance[key]))
#     print("-------------------------")
