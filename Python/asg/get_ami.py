import boto3
import pprint

def get_ami_list(ec2_client, ami_images):
    ami_list = ec2_client.describe_images(Owners=['self'])
    for ami in ami_list['Images']:
        ami_images.append(ami['Name'])


def main():
    ami_images = []
    ec2_client = boto3.client('ec2', region_name='us-west-2') # Change as appropriate
    get_ami_list(ec2_client, ami_images)

    # print(ami_images)

    for ami_id in ami_images:
        print(ami_id)

	# asg_with_notifications = []

	# asg_notifications = client.describe_notification_configurations(
	# 	AutoScalingGroupNames=asg_list,
	# 	MaxRecords=100)

	# more_asg_notifications = client.describe_notification_configurations(
	# 	NextToken=asg_notifications['NextToken'])
	# asg_with_notifications.append(asg_notifications)

	# asg_with_notifications.append(more_asg_notifications)

	# pp = pprint.PrettyPrinter(indent=2)

	# pp.pprint(asg_with_notifications)

if __name__ == '__main__':
	main()



# import boto3

# ec2_client = boto3.client('ec2', region_name='us-west-2') # Change as appropriate

# images = ec2_client.describe_images(Owners=['self'])

# for asg in asg_list['AutoScalingGroups']:
#     if (asg['AutoScalingGroupName']):
#         asgs.append(asg['AutoScalingGroupName'])
# return(asgs)

# for ami in images['AutoScalingGroups']:
#     if (ami['ImageId']):
#         asgs.append(asg['AutoScalingGroupName'])
# return(asgs)

# print(images)