import boto3

client = boto3.client('ec2', region_name='us-west-2')

response = client.replace_iam_instance_profile_association(
    IamInstanceProfile={
        'Arn': 'arn:aws:iam::590992000271:role/EdwardsEC2RoleforSSMandCWAgent',
        'Name': 'EdwardsEC2RoleforSSMandCWAgent'
    },
    AssociationId=
		'iip-assoc-09d308a05106fbce8',
		'iip-assoc-028ed8268b4375951',
		'iip-assoc-0983704d3dafb4103',
		'iip-assoc-034a9ab955f8ff69b',
		'iip-assoc-0eb7938fde4d420ca',
		'iip-assoc-000efe4c36742a37f',
		'iip-assoc-0b07d5de155772d21',
		'iip-assoc-0eaeb72729debcc9b',
		'iip-assoc-0a072aff98f1824d3',
		'iip-assoc-0a945b2fa18d45153',
		'iip-assoc-0a0f5508df9ce8fb2',
		'iip-assoc-06bfd7ce2e81e5ae0',
		'iip-assoc-02860e9c020e57d4c',
)

# arn_list = []

# for association in response['IamInstanceProfileAssociations']:
# 	print(association['AssociationId'])
# 	print(association['InstanceId'])
# 	print(association['IamInstanceProfile']['Arn'])
	# for profile in association['IamInstanceProfile']:
	# 	print(profile)
		# for arn in profile['Arn']:
		# 	print(arn['Key'])
			# print(arn[0])


# for reservations in response['Reservations']:
#     for instances in reservations['Instances']:
#         for tags in instances['Tags']:
#             if tags['Key'] == 'Name':
#                 print(tags['Value'])
#         print(instances['InstanceId'])


# 		arn_list.append(profile['Arn'])
# print(arn_list)


# print(response)