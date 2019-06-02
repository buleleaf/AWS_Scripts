import boto3
import argparse
import csv


# parser = argparse.ArgumentParser(prog='SG-to-csv', description='Audit Security Groups and append to csv.')

# # required
# parser.add_argument('-o', '--out', required=True, action='store', dest='output_file', type=str, help='path to where the ouput should be written.')

# args = parser.parse_args()


ec2_client = boto3.client('ec2')


sg_paginator = ec2_client.get_paginator('describe_security_groups')
sg_page_iterator = sg_paginator.paginate()

security_groups = {}
security_group_attachments = {}
for page in sg_page_iterator:
  for sg in page['SecurityGroups']:
    security_groups[sg['GroupId']] = sg
    security_group_attachments[sg['GroupId']] = []

print("Found {:d} security groups.".format(len(security_groups)))



# Print results
for sg_id, attachments in security_group_attachments.items():
  if not attachments:
    print("SG {} has no attachments! (Name: {})".format(sg_id, security_groups[sg_id]['GroupName']))


with open('SecurityGroup.csv', 'w') as csvfile:
    fieldnames = ['SecurityGroups'] + ['GroupId']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for page in sg_page_iterator:
        row = {}
        for sg_dict in page['SecurityGroups']:
            row[security_groups[sg_id]['GroupId']].values([0])
            # row[security_group_attachments]