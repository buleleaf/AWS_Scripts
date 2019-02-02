import boto3
import json
import pprint
client = boto3.client('ec2', region_name='us-west-1')

snapshots = client.describe_snapshots(
    Filters=[
        {
            'Name': 'owner-id',
            'Values': [
                '753955134882',

            ]
        }

    ]
)

for i in range(0, len(snapshots['Snapshots'])):
    print snapshots['Snapshots'][i]['VolumeId']

snap = snapshots['Snapshots'][i]['VolumeId']

for t in range(0, len(snap['Snapshots'][i]['VolumeId'])):

    print snap

# instance_volumes = client.describe_instances(
#             Filters=[
#                 {
#                     'Name': 'block-device-mapping.volume-id',
#                     'Values': [(snapshots['Snapshots'][i]['VolumeId']),
#
#                  ]
#              }
#
#          ]
#
#      )
#
#
# for v in range(0, len(instance_volumes['Reservations'])):
#     print instance_volumes['Reservations'][v]['Instances'][v]['InstanceId']
