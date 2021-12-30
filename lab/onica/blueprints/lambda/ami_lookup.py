"""Finds the latest AMI for a given platform - v1.1.0"""

import boto3
import cfnresponse  # pylint: disable=E0401


def handler(event, context):
    """ Lambda entry point """

    region = event['ResourceProperties']['Region']
    platform = event['ResourceProperties']['Platform']

    ami_filters = [
        {
            'Name': 'architecture',
            'Values': ['x86_64']
        },
        {
            'Name': 'is-public',
            'Values': ['true']
        },
        {
            'Name': 'root-device-type',
            'Values': ['ebs']
        },
        {
            'Name': 'state',
            'Values': ['available']
        },
        {
            'Name': 'virtualization-type',
            'Values': ['hvm']
        }
    ]
    ami_owners = []

    # Using naming conventions from
    # https://github.com/test-kitchen/kitchen-ec2/tree/master/lib/kitchen/driver/aws/standard_platform
    if platform == 'centos-7':
        ami_filters.extend([
            {
                'Name': 'owner-id',
                'Values': ['679593333241']
            },
            {
                'Name': 'product-code',
                'Values': ['aw0evgkw8e5c1q413zgy5pjce']  # CentOS 7
            }
        ])
        ami_owners = ['aws-marketplace']
    elif platform == 'ubuntu-16.04':
        ami_filters.extend([
            {
                'Name': 'name',
                'Values': ['ubuntu/images/*/ubuntu-*-16.04*']
            },
            {
                'Name': 'owner-id',
                'Values': ['099720109477']
            }
        ])
    # https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/walkthrough-custom-resources-lambda-lookup-amiids.html
    elif platform == 'amazon-hvm64':
        ami_filters.extend([
            {
                'Name': 'name',
                'Values': ['amzn-ami-hvm*x86_64-gp2']
            }
        ])
        ami_owners = ['amazon']
    elif platform == 'windows-2012r2':
        ami_filters.extend([
            {
                'Name': 'owner-alias',
                'Values': ['amazon']
            },
            {
                'Name': 'name',
                'Values': ['Windows_Server-2012-R2_RTM-English-*-Base-*',
                           'Windows_Server-2012-R2_SP*-English-*-Base-*']
            }
        ])

    client = boto3.client('ec2', region_name=region)

    describe_response = client.describe_images(
        ExecutableUsers=['all'],  # public images
        Owners=ami_owners,
        Filters=ami_filters
    )

    response_data = {}
    if 'Images' in describe_response and describe_response['Images'] != []:
        response_code = cfnresponse.SUCCESS
        # Get ami from last dict in the list of matching Images
        sorted_images = sorted(describe_response['Images'],
                               key=lambda k: k['Name'])
        latest_ami = sorted_images[-1]
        if platform.startswith('amazon-'):
            # Ensure rc images aren't included
            for i in reversed(sorted_images):
                if '.rc-' in latest_ami['Name']:
                    latest_ami = i
        response_data['ImageId'] = latest_ami['ImageId']
        response_data['Name'] = latest_ami['Name']
    else:
        response_code = cfnresponse.FAILED
        response_data['Data'] = describe_response['ResponseMetadata']

    cfnresponse.send(event,
                     context,
                     response_code,
                     response_data,
                     False)  # physicalResourceId
