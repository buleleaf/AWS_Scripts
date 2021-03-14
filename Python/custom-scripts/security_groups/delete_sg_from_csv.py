import os
import csv
from itertools import chain

with open('cloudwatch_logs.csv', 'r') as f:
    reader = csv.reader(f)
    security_groups = list(reader)

for sg in security_groups:
    print("\nChanging retention on Log Group: {}".format(str(sg)[2:-2]))
    os.system("aws ec2 delete-security-group --group-id {}".format(str(sg)[2:-2]))
    