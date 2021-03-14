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
		elif tag['Key'] != "StatelessHa":
			pass
	elif asg_list:
		asg_no_tag.append(asg_no_tag['AutoScalingGroupName'])

	
	
tagged_stateless = len(tag_list)

print(f"ASG's with Tag 'StatelessHa' = {tagged_stateless}")

print(asg_no_tag)