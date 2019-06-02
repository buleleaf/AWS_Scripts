import boto3 
import collections 
import datetime 
ec = boto3.client('ec2','us-east-1') #mention your region to reboot
to_tag = 0
def lambda_handler(event, context): 
 print "hi"
 reservations = ec.describe_volumes( Filters=[ {'Name': 'tag-key', 'Values': ['backup', 'True']}, ] )
 print(reservations)
 for volume in reservations['Volumes']:
    print "Backing up %s in %s" % (volume['VolumeId'], volume['AvailabilityZone'])
 
 # Create snapshot
 reservations = ec.create_snapshot(VolumeId=volume['VolumeId'],Description="Lambda backup for ebs" + volume['VolumeId'])
 
 result = reservations["SnapshotId"]
 print(result)
 
 ec.create_tags(
 Resources=[result],Tags=[
 {'Key': 'Name', 'Value': 'snapshot' },
 ]
 )