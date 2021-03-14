import boto3

region = 'us-west-2'

client = boto3.client('rds', region_name=region)

response = client.add_tags_to_resource(
    ResourceName='arn:aws:rds:us-west-2:590992000271:db:awor-pdrdsmys01',
    Tags=[
        {
            'Key': 'Environment',
            'Value': 'Production'
        },
        {
            'Key': 'ContactPreference',
            'Value': 'Email'
        },
        {
            'Key': 'Managed',
            'Value': 'No'
        },
        {
            'Key': 'Application',
            'Value': 'n/a'
        },
        {
            'Key': 'CostCenter',
            'Value': 'n/a'
        },
        {
            'Key': 'RequestNumber',
            'Value': 'n/a'
        },
        {
            'Key': 'ReviewDate',
            'Value': 'n/a'
        },
        {
            'Key': 'ServiceOwner',
            'Value': 'n/a'
        },
        {
            'Key': 'TechnicalOwner',
            'Value': 'n/a'
        },
    ]
)
