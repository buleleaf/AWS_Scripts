# pip install boto3

import boto3
import json

region = 'us-west-2'

client = boto3.client('imagebuilder', region_name=region)

response = client.create_image_recipe(
    name='encrypted-sdk-image',
    description='created from SDK',
    semanticVersion='2.0.0',
    components=[
        {
            'componentArn': 'arn:aws:imagebuilder:us-west-2:753955134882:component/cwagentinstall/2.0.0/1'
        },
    ],
    parentImage='ami-08cfff638ed01c591',
    blockDeviceMappings=[
        {
            'deviceName': '/dev/sda1',
            'ebs': {
                'encrypted': True,
                'deleteOnTermination': False,
                'kmsKeyId': 'b67c0139-c255-4723-8452-6c073d514a46',
                'volumeSize': 100,
                'volumeType': 'gp2'
            },
        },
    ],
    # Please note no tag can be name.
    # tags={
    #     'name': '{customer}-{name}'.format(**args)
    # }
)


print(response)