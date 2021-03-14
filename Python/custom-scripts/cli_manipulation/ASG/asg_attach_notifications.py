import os
import csv
from itertools import chain

with open('asg.csv', 'r') as f:
    reader = csv.reader(f)
    security_groups = list(reader)

for sg in security_groups:
    print("\nAdding Scaling Notification to ASG: {}".format(str(sg)[2:-2]))
    os.system("aws autoscaling put-notification-configuration --auto-scaling-group-name {} --topic-arn arn:aws:sns:us-west-2:590992000271:edwards-scaling-topic --notification-types \"autoscaling:EC2_INSTANCE_LAUNCH\" \"autoscaling:EC2_INSTANCE_LAUNCH_ERROR\" \"autoscaling:EC2_INSTANCE_TERMINATE\" \"autoscaling:EC2_INSTANCE_TERMINATE_ERROR\"".format(str(sg)[2:-2]))
    

