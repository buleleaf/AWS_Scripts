import boto3
import pprint

def get_asg_list(client):
	asgs = []
	asg_list = client.describe_auto_scaling_groups(
		MaxRecords=100)
	for asg in asg_list['AutoScalingGroups']:
		if (asg['AutoScalingGroupName']):
			asgs.append(asg['AutoScalingGroupName'])
	return(asgs)

def main():

	client = boto3.client('autoscaling')
	asg_list = get_asg_list(client)

	print(asg_list)

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
