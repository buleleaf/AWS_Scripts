#!/usr/bin/env python3
"""Validate that all instances are able to be patched."""
import argparse
import csv
import boto3
import botocore.exceptions


def parse_opts():
    """Help messages (-h, --help)."""
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument('-r', '--region', type=str, help='AWS Region',
                        default='us-west-2')
    parser.add_argument('-c', '--patch_csv', type=str,
                        help='Path to your Patching CSV file.')
    return parser.parse_args()


def _get_instance_list(filename):
    with open(filename, 'r') as infile:
        reader = csv.DictReader(infile)
        return [r for r in reader]


def main():
    """Main."""
    args = parse_opts()
    instances = _get_instance_list(args.patch_csv)
    client = boto3.client('ec2', region_name=args.region)
    for index, instance in enumerate(instances):
        for key in ('InstanceName', 'InstanceId'):
            if key not in instance:
                print('Index {} is missing {}'.format(index, key))
        try:
            client.describe_instances(InstanceIds=[instance['InstanceId']])
        except botocore.exceptions.ClientError as error:
            print(error)


if __name__ == '__main__':
    main()
