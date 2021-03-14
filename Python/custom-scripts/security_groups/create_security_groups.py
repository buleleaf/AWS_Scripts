import os
import csv


with open('sg_name.csv', 'r') as f:
    reader = csv.reader(f)
    sg_name = list(reader)


# security_groups = ['sg-0676add0ee71cacbb','sg-0f947c509fae16c84','sg-01471a8e2ed4b5c9c',
#                     'sg-00a5c7ab4dcc52eef','sg-0526a8f2243d196ab','sg-9d7a80ef']

for sg in sg_name:
    os.system("aws ec2 create-security-group --group-name {} --description \"My security group\" > created_sg.json".format(sg))
