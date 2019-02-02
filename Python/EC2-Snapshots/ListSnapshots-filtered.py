#!/usr/local/bin/python
# By: Kyle Finley
# Description: Creates a CSV of all snapshots in an AWS account for auditing
import boto3
from botocore.client import Config
import csv
#- Enables support for multiple Named Profiles -#
profile = None
session = None
while session == None:
    profile = raw_input('AWS Named Profile: ') #user prompt
    try: #validates profile
        session = boto3.session.Session(profile_name=profile)
    except Exception:
        print 'AWS Named Profile "%s" was not found.' % profile
        session = None
TagFilter = [
    "Name",
    "Application",
    "ApplicationTier",
    "BusinessOwner",
    "CostCenter",
    "Environment",
    "ProjectName",
    "ProjectYear",
    "ServiceOwner",
    "TechnicalOwner"
]
#- Setting up boto -#
boto3config = Config(connect_timeout=50, read_timeout=300) #extends timeout
ec2 = session.client('ec2', config=boto3config)
paginator = ec2.get_paginator('describe_snapshots')
OwnerId = str(session.client('sts').get_caller_identity().get('Account')) #gets root account ID
#- Configure botocore retries -#
## This paired with the long timeout supports a large number of snapshots
unique_handlers = ec2.meta.events._unique_id_handlers
checker = unique_handlers['retry-config-ec2']['handler']._checker
checker.__dict__['_max_attempts'] = 20
#- Collecting Snapshots -#
snap_data = list() #stores data for all snapshots

response_iterator = paginator.paginate(
    OwnerIds=[OwnerId], #required for accurate and fast response
    PaginationConfig={
        'PageSize': 500 #lowers the chance of timeout
    }
)
#- Processing Snapshots -#
for page in response_iterator:
    for snapshot in page['Snapshots']:
        data = {'SnapshotId' : snapshot['SnapshotId'], 'VolumeId' : snapshot['VolumeId'], 'StartTime' : snapshot['StartTime']} #creates a dict to keep data together
        if 'Tags' in snapshot: #some snapshots dont have tags
            TagList = list()
            for tag in snapshot['Tags']:
                TagList.append(tag['Key'])
            if not all(TagFilter) in TagList:
                data['Tags'] = snapshot['Tags']
                snap_data.append(data)
        else:
            snap_data.append(data)
#- Output -#
with open('SnapshotOutput.csv', 'wb') as f: #name of file saved to same directory as script
    for item in snap_data:
        w = csv.DictWriter(f, item.keys())
        w.writerow(item)
    f.close()
print 'Snapshots found: %i' % len(snap_data) #shows number of snapshots in terminal
