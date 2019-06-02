#!/usr/bin/env python

import boto3
import botocore
import argparse
import unicodecsv as csv

# parse command line argumetns
def parse_args():
    parser = argparse.ArgumentParser(prog='tags-to-csv', description='Get snapshot tags in CSV format.')
    # required
    parser.add_argument('-o', '--out', required=True, action='store', dest='output_file', type=str, help='path to where the output should be written')

    # optional
    parser.add_argument('-r', '--region',action='store', default='us-east-1', dest='aws_region', type=str, help='AWS region to use.')
    parser.add_argument('-v', '--version', action='version', version='0.1')

    args = parser.parse_args()
    return args

def get_snapshots(filters=[]):
    reservations = {}
    try:
        reservations = ec2.describe_snapshots(
            Filters=filters
        )
    except botocore.exceptions.ClientError as e:
        print e.response['Error']['Message']

    snapshots = []
    for reservation in reservations.get('Reservations', []):
        for snapshot in reservation.get('Snapshots', []):
            snapshots.append(snapshot)
    return snapshots

#
# Main
#
def main():
    global args
    global ec2

    args = parse_args()
    
    ec2 = boto3.client('ec2', region_name=args.aws_region)

    snapshots = get_snapshots()

    tag_set = []
    for snapshot in snapshots:
        for tag in snapshot.get('Tags', []):
            if tag.get('Key'):
                tag_set.append(tag.get('Key'))
    tag_set = list(set(tag_set))

    with open(args.output_file, 'w') as csvfile:
        fieldnames = ['SnapshotId'] + tag_set
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for snapshot in snapshots:
            row = {}
            for tag in snapshot.get('Tags', []):
                row[tag.get('Key')] = tag.get('Value')
            row['SnapshotId'] = snapshot.get('SnapshotId')
            writer.writerow(row)

if __name__ == "__main__":
    main()