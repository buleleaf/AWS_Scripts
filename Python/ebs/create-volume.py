
import boto3

region = 'us-west-2'

ec2client = boto3.client('ec2', region_name=region)

response = client.create_volume(
    AvailabilityZone='region',
    # Encrypted=True|False,
    # Iops=123,
    # KmsKeyId='string',
    # OutpostArn='string',
    # Size=123,
    SnapshotId='snap-09adcc2b712086452',
    VolumeType='gp2',
    TagSpecifications=[
        {
            'ResourceType': 'volume',
            'Tags': [
                {
                "Key": "Application",
                "Value": "Windchill"
                },
                {
                "Key": "ApplicationTier",
                "Value": "Application"
                },
                {
                "Key": "ApplicationTierLevel",
                "Value": "No Tier"
                },
                {
                "Key": "ContactPreference",
                "Value": "Email"
                },
                {
                "Key": "CorpInfoMSP:TakeNightlySnapshot",
                "Value": "Yes"
                },
                {
                "Key": "CostCenter",
                "Value": "1001596013"
                },
                {
                "Key": "Environment",
                "Value": "Development"
                },
                {
                "Key": "Managed",
                "Value": "Yes"
                },
                {
                "Key": "MonitoredServices",
                "Value": "No"
                },
                {
                "Key": "Name",
                "Value": 'AWOR-DVPDMLAS10'
                },
                {
                "Key": "PatchGroup",
                "Value": "ProductionManualReboot"
                },
                {
                "Key": "Purpose",
                "Value": "CAD PLM"
                },
                {
                "Key":"RequestNumber",
                "Value":"RITM0122480"
                },
                {
                "Key": "ReviewDate",
                "Value": "8/1/2021"
                },
                {
                "Key": "Schedule",
                "Value": "AlwaysOn"
                },
                {
                "Key": "ServiceLocation",
                "Value": "Irvine"
                },
                {
                "Key": "ServiceOwner",
                "Value": "Amir Memaran"
                },
                {
                "Key": "TechnicalOwner",
                "Value": "Mike Lockwood"
                },
                {
                "Key": "Validated",
                "Value": "No"
                }
            ]
        }

