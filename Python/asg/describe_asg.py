import boto3
import pprint

region = 'us-west-2'

asg = boto3.client('autoscaling', region_name=region)
response = asg.describe_auto_scaling_groups()

tag_list = []
asg_no_tag = []
for asg_list in response['AutoScalingGroups']:
	for tag in asg_list['Tags']:
		if tag['Key'] == "StatelessHa":
			tag_list.append(tag['Key'])
		# else:
		# 	print("no tags with that key")

# for asg_list2 in response['AutoScalingGroups']:
# 	for no_tag in asg_list2['Tags']:
# 		if tag['Key'] != "StatelessHa":
# 			asg_without_tag = asg.describe_auto_scaling_groups()
# 			print(asg_without_tag)


		# print(f"{tag['Key']} " + tag['Value']) # this prints the key value pair of the tag
	
tagged_stateless = len(tag_list)

print(f"ASG's with Tag 'StatelessHa' = {tagged_stateless}")

# print(asg_no_tag)




# pp = pprint.PrettyPrinter(indent=1)

# pp.pprint(response)