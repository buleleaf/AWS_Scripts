import csv
import boto3
import pprint

# asg_list = [
# 'AWOR-PDMESCIO01-ASG',
# 'AWOR-PDORAAPX01-asg',
# 'AWOR-PDQLKGEO01-asg',
# 'AWOR-PDQMSWEB02-asg',
# 'AWOR-QALABAPP01-asg',
# 'AWOR-TSDWHAPP01-asg',
# 'AWOR-TSOLAPDB01-asg',
# 'AWOR-TSOLAPPB01-asg',
# 'AWOR-TSPDMLAS01-asg',
# 'AWOR-TSSASAPP01-asg',
# 'AwOr-PdMovXfr01-asg',
# 'AwOr-TsMovApp01-asg',
# 'IRVDIGWEB13-asg',
# 'IRVHFMFDM02-asg',
# 'IRVINE724-asg',
# 'IRVINE739-asg',
# 'IRVLBLPRG01-asg',
# 'IRVLBLPRG02-asg',
# 'IRVLBLSPC01-asg',
# 'IRVMETCAL02-asg',
# 'IRVOLBECM01-PRD-asg',
# 'IRVOLBECM01-QA-asg',
# 'IRVOLBSCH01-PRD-asg',
# 'IRVOLBSCH01-QA-asg',
# 'IRVORACLN11-asg',
# 'IRVORACLN12-asg',
# 'IRVORACLN14-asg',
# 'IRVORACLN15-asg',
# 'IRVQMSAPP01-asg',
# 'IRVTHVSAS01-asg',
# 'IRVVALGEN01-asg',
# 'IrvITRSPT04-asg',
# 'IrvLABAPP02-asg',
# 'IrvLABSCH02-asg',
# 'IrvQMSWEB01-asg',
# 'Irvine837-asg',
# 'Irvine882-asg',
# 'Irvine902-asg',
# 'asadmin-common-fe-proxy-asg-ProxyServerASG-Z68E5W7PLU43',
# 'awor-qalabapp02-asg',
# 'awor-tswplapp01-asg',
# 'edwards-prod-ibcm-fe-proxy-asg-ProxyServerASG-5JTOPR2O9CYS',
# 'edwards-prod-qlik-fe-proxy-asg-ProxyServerASG-K9NW3CEF93GH',
# 'edwards-test-exch-fe-proxy-asg-ProxyServerASG-OSAN5QUPF3BY',
# 'irvjdemex02-asg',
# 'irvjdepit07-asg',
# 'irvlabapp01-asg',
# 'irvlblspc01-oq-asg',
# 'AWOR-DVMESWRK01-ASG']

# test_list = ['lab1', 'dmlab-common-core-vpnserver-VPNServerASG-XUIAMNKXXFF']

# client = boto3.client('autoscaling')
# for asgs in test_list:
# 	client.put_notification_configuration(
# 	AutoScalingGroupName=asgs,
# 	# TopicARN='arn:aws:sns:us-west-2:590992000271:edwards-scaling-topic',
# 	TopicARN='arn:aws:sns:us-west-2:753955134882:Topic1',
# 	NotificationTypes=[
# 		'autoscaling:EC2_INSTANCE_LAUNCH',
# 		'autoscaling:EC2_INSTANCE_LAUNCH_ERROR',
# 		'autoscaling:EC2_INSTANCE_TERMINATE',
# 		'autoscaling:EC2_INSTANCE_TERMINATE_ERROR',
# ]
# )

# print(asgs)

# def get_asg_list(client):
client = boto3.client('autoscaling')

# with open('test.csv', 'r') as f:
with open('asg_no_notifications.csv', 'r') as f:
	reader = csv.reader(f)
	asg_no_notifications = list(reader)



for asgs in asg_no_notifications:
	for asg in asgs:
		client.put_notification_configuration(
			AutoScalingGroupName=asg,
			TopicARN='arn:aws:sns:us-west-2:590992000271:edwards-scaling-topic',
			# TopicARN='arn:aws:sns:us-west-2:753955134882:Topic1',
			NotificationTypes=[
				'autoscaling:EC2_INSTANCE_LAUNCH',
				'autoscaling:EC2_INSTANCE_LAUNCH_ERROR',
				'autoscaling:EC2_INSTANCE_TERMINATE',
				'autoscaling:EC2_INSTANCE_TERMINATE_ERROR',
			]
		)
print(asg)

# for asgs in asg_no_notifications:
# 	client.put_notification_configuration(
# 	AutoScalingGroupName=asgs,
# 	# TopicARN='arn:aws:sns:us-west-2:590992000271:edwards-scaling-topic',
# 	TopicARN='arn:aws:sns:us-west-2:753955134882:Topic1',
# 	NotificationTypes=[
# 		'autoscaling:EC2_INSTANCE_LAUNCH',
# 		'autoscaling:EC2_INSTANCE_LAUNCH_ERROR',
# 		'autoscaling:EC2_INSTANCE_TERMINATE',
# 		'autoscaling:EC2_INSTANCE_TERMINATE_ERROR',
# ]
# )

# print(asgs)
	# return(asg_no_notifications)

	# f = open('asg_2.txt', 'r')

# f = open('test.txt', 'r')

	# output = f.read()


# print(output)

# def main():
	
# 	client = boto3.client('autoscaling')
# 	asg_list = get_asg_list(client)
# 	length = len(asg_list)

# 	for i in range(length):
# 		print(asg_list[i])


# 	asg_pnc = client.put_notification_configuration(
# 		AutoScalingGroupName=new_list,
# 		TopicARN='arn:aws:sns:us-west-2:590992000271:edwards-scaling-topic',
# 		# TopicARN='arn:aws:sns:us-west-2:753955134882:Topic1',
# 		NotificationTypes=[
# 			'autoscaling:EC2_INSTANCE_LAUNCH',
# 			'autoscaling:EC2_INSTANCE_LAUNCH_ERROR',
# 			'autoscaling:EC2_INSTANCE_TERMINATE',
# 			'autoscaling:EC2_INSTANCE_TERMINATE_ERROR',
# 	]
# )

# 	print(asg_pnc)

# if __name__ == '__main__':
# 	main()
