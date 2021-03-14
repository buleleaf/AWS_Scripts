import boto3

region = 'us-west-2'

client = boto3.client('ec2', region_name=region)

response = client.add_tags_to_resource(
    ResourceName='arn:aws:rds:us-west-2:590992000271:db:awor-pdrmndb01',
    Tags=[
        {
            'Key': 'PatchGroup',
            'Value': 'ProductionManualReboot'
        },
        {
            'Key': 'CorpInfoMSP:TakeNightlySnapshot',
            'Value': 'No'
        },
        {
            'Key': 'Managed',
            'Value': 'No'
        },
        # {
        #     'Key': '',
        #     'Value': ''
        # },
        # {
        #     'Key': '',
        #     'Value': ''
        # },
        # {
        #     'Key': '',
        #     'Value': ''
        # },
    ]
)
