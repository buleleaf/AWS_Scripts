#!/usr/local/bin/python
# By: Kyle Finley
# Description: Creates a CSV of all snapshots related to AMIs in an AWS account for auditing
# TODO add checks to see if AMI is in use by an launch configuration
# TODO add checks to see if any instances have been launched with AMI

import boto3
from botocore.client import Config
import csv
from dateutil.parser import parse
import datetime
import os
from collections import OrderedDict
ordered_fieldnames = OrderedDict([('AmiName',None),('ImageId',None),('CreationDate', None),('SnapshotId',None),('SnapshotVolumeSize',None),('SnapshotTags',None)])

def clear():
    os.system('cls' if os.name == 'nt' else 'clear') #clears screen
clear()
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

# #- Read AMI IDs from CSV -#
# csvIds = list() #ids found in csv
# print 'Please enter the path to your csv file including file extension.'
# file_path = str(raw_input('Path: ')) #user prompt
# #id_key = str(raw_input('Header used for AMI IDs: '))
# try:
#     with open(file_path, 'rU') as csvFile:
#         reader = csv.reader(csvFile)
#         for row in reader:
#             ami_id = str(row[0]).split(" ")[0]
#             csvIds.append(ami_id)
# except Exception as e:
#     print 'File path invalid or key not found.'
#     print e
# print 'Found %i AMI IDs in CSV file' % len(csvIds)

def find_snapshot(snapId, snapshots):
    for snap in snapshots:
        if snap.get('SnapshotId') == snapId:
            return snap

#- Processing AMIs -#
print 'Getting AMIs data...'
snap_data = list()
response = ec2.describe_images(Owners=[OwnerId])
allSnapshots = ec2.describe_snapshots(OwnerIds=[OwnerId])['Snapshots']
for ami in response["Images"]:
    print 'Processing {}...'.format(ami['ImageId'])
    for volume in ami['BlockDeviceMappings']:
        if not 'VirtualName' in volume:
            if 'SnapshotId' in volume['Ebs']:
                data = {}
                snapId = volume['Ebs']['SnapshotId']
                snapshot = find_snapshot(snapId, allSnapshots)

                data['SnapshotId'] = snapId
                data['ImageId'] = ami['ImageId']
                data['CreationDate'] = ami['CreationDate']
                data['AmiName'] = ami['Name']
                data['SnapshotVolumeSize'] = snapshot.get('VolumeSize')
                data['SnapshotTags'] = str(snapshot.get('Tags'))
                snap_data.append(data)
# print 'Found %i snapshots associated with AMIs not created this year' % len(snap_data)

#- Output -#
print 'Writing data to file...'
with open('SnapshotOutput.csv', 'wb') as f: #name of file saved to same directory as script
    w = csv.DictWriter(f, fieldnames=ordered_fieldnames)
    w.writeheader()
    for item in snap_data:
        w.writerow(item)
    f.close()
print 'Finished writing to file: SnapshotOutput.csv'
