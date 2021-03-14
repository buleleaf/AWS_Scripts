import sys
import boto3
from botocore.exceptions import ClientError
import logging
import argparse


if __name__ == '__main__':
    response = []
    paginator = boto3.client('ec2').get_paginator('describe_instances')
    page = paginator.paginate()
    for p in page:
         for ec in p['Reservations']:
            for e in ec['Instances']:
                r = e['IamInstanceProfile']
                response.append(r)
    print response
