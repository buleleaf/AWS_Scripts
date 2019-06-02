# #################
# Description: List all snapshots for a region, grouped by ec2 instance.
# JIRA-177
# Input: Region
# Output: Listing of all snapshots in the following format:
#         <tag "Name"> ; <snapshot id> ; <create date>
#         CSV mode outputs in the following format:
#         <tag "Name">,<instance id>,ec2_snapshot,<vol id>,<latest snap date>
# Version: v1.1
# Author: Michael Bordash (mbordash@onica.com)
# #################

"""Description: List all snapshots for a region, grouped by ec2 instance."""

import argparse
import boto3

REGIONS = [
    "ap-south-1",
    "eu-west-3",
    "eu-west-2",
    "eu-west-1",
    "ap-northeast-2",
    "ap-northeast-1",
    "sa-east-1",
    "ca-central-1",
    "ap-southeast-1",
    "ap-southeast-2",
    "eu-central-1",
    "us-east-1",
    "us-east-2",
    "us-west-1",
    "us-west-2"
]

PARSER = argparse.ArgumentParser(usage='%(prog)s [-h] [-v] [-csv] region',
                                 description="Description: List snapshots" +
                                 "for the ec2 instances in specified region")
PARSER.add_argument("region", choices=REGIONS, type=str,
                    help="Region to run against.")
PARSER.add_argument("-v", "--verbose", action="store_true",
                    help="Output all snapshot details.")
PARSER.add_argument("-csv", action="store_true",
                    help="Generate CSV formatted output.")
ARGS = PARSER.parse_args()

# input value for region to process
# REGION = ARGS.region

# color constants for terminal output
RED = '\033[0;31m'  # instance id
GREEN = '\033[0;32m'  # volume id
YELLOW = '\033[0;33m'  # snapshot details
BLUE = '\033[0;34m'  # region
NC = '\033[0m'


print "Running against region: {}{}{}".format(BLUE, ARGS.region, NC)
# create an ec2 client
EC2CLIENT = boto3.client('ec2', region_name=ARGS.region)


# call describe_instances on the client object to get JSON response
# response = EC2CLIENT.describe_instances()
EC2_PAGINATOR = EC2CLIENT.get_paginator('describe_instances')
EC2_RESPONSE_ITERATOR = EC2_PAGINATOR.paginate()

# instance and snapshot counters
INSTCNTR = 0
SNAPCNTR = 0

# iterate through the instances and print out the volumes and their snaps
for page_of_reservations in EC2_RESPONSE_ITERATOR:
    for reservation in page_of_reservations["Reservations"]:
        for instance in reservation["Instances"]:
            INSTCNTR += 1
            if not ARGS.csv:
                # logic to grab tagname
                if 'Tags' in instance:
                    tags = instance["Tags"]
                    for tag in tags:
                        if tag['Key'] == 'Name':
                            EC2NameTag = tag['Value']
                            break
                        else:
                            EC2NameTag = "No Name Defined"
                else:
                    EC2NameTag = "No Tag Name Found"
                print("Snapshot list for instance: {} ({}{}{})"
                      .format(EC2NameTag, RED, instance["InstanceId"], NC))
            for devices in instance["BlockDeviceMappings"]:
                VolId = devices["Ebs"]["VolumeId"]
                if not ARGS.csv:
                    print(" -Instance id: {}{}{} ; Volume id: {}{}{}"
                          .format(RED, instance["InstanceId"], NC, GREEN,
                                  VolId, NC))
                snap_paginator = EC2CLIENT.get_paginator('describe_snapshots')
                snap_response_iterator = snap_paginator.paginate(
                    Filters=[{'Name': 'volume-id', 'Values': [VolId]}])
                if ARGS.csv:  # define a list to use for snapshots for csv mode
                    snap_list = []
                for page_of_snapshots in snap_response_iterator:
                    for snapshot in page_of_snapshots["Snapshots"]:
                        if 'Tags' in snapshot:
                            tags = snapshot["Tags"]  # list of dictionaries
                            for tag in tags:
                                if tag['Key'] == 'Name':
                                    SnapNameTag = tag['Value']
                                    break
                                else:
                                    SnapNameTag = 'No Name Defined'
                        else:
                            SnapNameTag = "No Tag Name Found"
                        if not ARGS.csv and ARGS.verbose:
                            print(("  -Snapshot name: {}{}{} ; Snapshot id: "
                                   "{}{}{} ; Start time: {}{}{}")
                                  .format(YELLOW, SnapNameTag, NC, YELLOW,
                                          snapshot["SnapshotId"], NC, YELLOW,
                                          snapshot["StartTime"], NC))
                        SNAPCNTR += 1
                        if ARGS.csv:
                            snap_list.append(snapshot["StartTime"])
                if not ARGS.csv:
                    print("  Number of snapshots processed for [{}{}{}]: {}\n"
                          .format(GREEN, VolId, NC, SNAPCNTR))
                else:
                    if snap_list:
                        snap_list.sort()
                        latest_snapshot_date = snap_list.pop()
                    else:
                        latest_snapshot_date = "No snapshot(s) present"
                        print("{},{},ec2_snapshot,{},{}"
                            .format(SnapNameTag, instance["InstanceId"],
                                    VolId, latest_snapshot_date))

                SNAPCNTR = 0

print "**Total number of instances processed**: " + str(INSTCNTR)
