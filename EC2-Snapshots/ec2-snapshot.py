#!/usr/bin/env python

import boto3
from botocore.client import Config
import csv
from dateutil.parser import parse
import datetime
import os
from collections import OrderedDict
ordered_fieldnames = OrderedDict([('CreationDate', None),('SnapshotId',None),('SnapshotVolumeSize',None),('SnapshotTags',None)])

ec2 = boto3.client('ec2', region_name='us-west-2')

paginator = ec2.get_paginator('describe_snapshots')

def find_snapshots(snapId, snapshots):
    for snap in snapshots:
        if snap.get('SnapshotId') == snapId:
            return snap


snap_data = list()
for snap in snapshots:
    if 'SnapshotId' in volume['Ebs']:
        data = {}
        snapId = volume['Ebs']['SnapshotId']
        snapshot = find_snapshot(snapId, allSnapshots)

        data['SnapshotTags'] = str(snapshot.get('Tags'))
        snap_data.append(data)

print 'Writing data to file...'
with open('SnapshotOutput.csv', 'wb') as f: #name of file saved to same directory as script
    w = csv.DictWriter(f, fieldnames=ordered_fieldnames)
    w.writeheader()
    for item in snap_data:
        w.writerow(item)
    f.close()
print 'Finished writing to file: SnapshotOutput.csv'
