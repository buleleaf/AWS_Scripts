#!/usr/bin/env python
"""Retrieve tags from ec2 instances and list tags missing."""
# Can you work on a script that will look at all ec2s and list what resources
# are missing tag. The tag keys are Company, Environment, Application,
# CostCenter.

import logging
import argparse
import csv
import boto3
import tabulate

__VERSION__ = '0.0.2'
FORMAT = "%(asctime)-15s %(levelname)s %(module)s.%(funcName)s %(message)s"
DATEFMT = "%Y-%m-%d %H:%M:%S"
logging.basicConfig(level=logging.INFO, format=FORMAT, datefmt=DATEFMT)
logging.getLogger('botocore').setLevel(logging.ERROR)
DEFAULT_WANTED_TAGS = ['Company', 'Environment', 'Application',
                       'CostCenter', 'Name']


def parse_opts():
    """Parse CLI Args."""
    parser = argparse.ArgumentParser(description='Tag Auditing.')
    group = parser.add_mutually_exclusive_group(required=True)
    regions = list(get_regions())
    group.add_argument('-r', '--region', type=str, action='store',
                       metavar='region', choices=regions,
                       help='Available regions: {}'.format(regions))
    group.add_argument('-a', '--all-regions', action='store_true')

    parser.add_argument('-w', '--wanted_tags', metavar='Tag',
                        action='append',
                        help='Wanted Tags; Default: {}'.format(
                            DEFAULT_WANTED_TAGS),
                        default=DEFAULT_WANTED_TAGS)
    parser.add_argument('-c', '--csv', metavar='Output file', type=str,
                        action='store',
                        help='Output filename for csv')
    parser.add_argument('-V', '--version', action='version',
                        version='%(prog)s {}'.format(__VERSION__))
    return parser.parse_args()


def get_regions():
    """Retrieve list of available EC2 Regions."""
    ec2 = boto3.client('ec2', region_name='us-west-2')
    return (region['RegionName']
            for region in ec2.describe_regions()['Regions'])


def get_missing_tags_region(wanted_tags, region):
    """Retrieve missing tags of instances by region."""
    missing_tags = {}  # organized by instance id, list of missing tags.
    ec2 = boto3.client('ec2', region_name=region)
    instances = ec2.describe_instances()
    for reservation in instances['Reservations']:
        for instance in reservation['Instances']:
            logging.debug('Process instance %s', instance['InstanceId'])
            tags = {tag['Key']: tag.get('Value', None)
                    for tag in instance['Tags']}
            logging.debug('Found %s tags', ', '.join(tags.keys()))
            missing_tags[instance['InstanceId']] = []
            for tag in wanted_tags:
                if tag not in tags.keys():
                    tags[tag] = '{}_MISSING'.format(tag)
            tags['InstanceId'] = instance['InstanceId']
            tags['region'] = region
            missing_tags[instance['InstanceId']] = tags
    return missing_tags


def main():
    """Main."""
    args = parse_opts()
    missing_tags = {}  # organized by instance id, list of missing tags.
    if args.all_regions:
        for region in get_regions():
            logging.info('Processing %s', region)
            missing_tags.update(
                **get_missing_tags_region(args.wanted_tags, region))
    else:
        missing_tags = get_missing_tags_region(args.wanted_tags, args.region)

    if args.csv:
        with open(args.csv, 'w') as outfile:
            fieldnames = set()
            for fields in missing_tags.values():
                fieldnames.update(set(fields.keys()))
            writer = csv.DictWriter(outfile, fieldnames=list(fieldnames))
            writer.writeheader()
            for row in missing_tags.values():
                writer.writerow(row)
    else:
        print(tabulate.tabulate(missing_tags.values(), headers='keys',
                                tablefmt='psql'))


if __name__ == '__main__':
    main()
