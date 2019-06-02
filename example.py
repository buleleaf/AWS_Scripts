import boto3
import defaultdict

ec2 = boto3.resource('ec2')
ec2_filter = [{'Name': 'intance_name', 'Values': ['stopped']}]

ec2.instances.filter(Filters=ec2_filter).start()
