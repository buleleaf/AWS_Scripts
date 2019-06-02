#!/usr/bin/env python3

# Simple script to figure out how many SGs we have that aren't being used.
# If it proves fruitful, I might make it more intelligent and see if we can
# safely delete some of them.

import boto3

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