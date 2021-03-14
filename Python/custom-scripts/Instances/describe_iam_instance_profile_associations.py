import boto3

client = boto3.client('ec2', region_name='us-west-2')

response = client.describe_iam_instance_profile_associations(
	Filters=[
		{
			'Name': 'instance-id',
			'Values': [
				'i-0ae3f63791af9e181',
				'i-02e0f7f9046df500d',
				'i-0b1c7e5a2cd51d518',
				'i-018d27468e5bd8cd0',
				'i-0d8deed45eb72c59d',
				'i-0bd92ca0b8fe0c577',
				'i-0c525be5cdef298c4',
				'i-03eaaed9a0f11a20e',
				'i-032f67f88d605953e',
				'i-0ba503eca0c009f5b',
				'i-024fdefdda6363545',
				'i-01ce8684bf9976a50',
				'i-0937fa4dd69c42421',
			]
		}
	]
)

for association in response['IamInstanceProfileAssociations']:
	print(association['AssociationId'])
	print(association['InstanceId'])
	print(association['IamInstanceProfile']['Arn'])
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