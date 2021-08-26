#!/usr/bin/env python3
import boto3
import botocore
import json
import re
import argparse

def boto3_client(resource):
    """Create Boto3 client."""
    return boto3.client(resource)


def s3_list_buckets():
    """Gets all S3 buckets and adds to a set"""
    bucket_list = set()
    s3_bucket = boto3_client('s3').list_buckets()
    for buckets in s3_bucket['Buckets']:
        bucket_list.add(buckets['Name'])
    return bucket_list


def s3_add_tags(tags,buckets):
    """Puts S3 Bucket tagging"""
    boto3_client('s3').put_bucket_tagging(Bucket=buckets,Tagging=tags)


def s3_filter_prod():
    """Filters bucket list by environment"""
    bucket_list = []
    prod = re.compile("prod-|-prod$")
    yield list(filter(prod.search, s3_list_buckets()))


def s3_add_tags_prod(file, env):
    """Adds tags to bucket based on file and environment"""
    tags_file = open(file)
    tags = json.load(tags_file)
    for bucket_filter in s3_filter_prod():
        for buckets in bucket_filter:
            if env == 'prod':
                s3_add_tags(tags,buckets)


def s3_filter_preview():
    """Filters bucket list by environment"""
    preview = re.compile("preview-|-preview$")
    yield list(filter(preview.search, s3_list_buckets()))


def s3_add_tags_preview(file, env):
    """Filters bucket list by environment"""
    tags_file = open(file)
    tags = json.load(tags_file)
    for bucket_filter in s3_filter_preview():
        for buckets in bucket_filter:
            if env == 'preview':
                s3_add_tags(tags,buckets)


def s3_filter_dev():
    """Filters bucket list by environment"""
    dev = re.compile("dev-|-dev$")
    yield list(filter(dev.search, s3_list_buckets()))


def s3_add_tags_dev(file, env):
    """Filters bucket list by environment"""
    tags_file = open(file)
    tags = json.load(tags_file)
    for bucket_filter in s3_filter_dev():
        for buckets in bucket_filter:
            if env == 'dev':
                s3_add_tags(tags,buckets)


def s3_filter_qa():
    """Filters bucket list by environment"""
    qa = re.compile("qa-|-qa$")
    yield list(filter(qa.search, s3_list_buckets()))


def s3_add_tags_qa(file, env):
    """Filters bucket list by environment"""
    tags_file = open(file)
    tags = json.load(tags_file)
    for bucket_filter in s3_filter_qa():
        for buckets in bucket_filter:
            if env == 'qa':
                s3_add_tags(tags,buckets)


def main():
    parser = argparse.ArgumentParser(prog='json-to-tags', description='Puts tags to S3 buckets from a JSON file. WARNING: This will remove any tags that already exist that are not specified.')
    parser.add_argument('-i', '--in', required=True, action='store', dest='input_file', type=str, help='path to where the input file is located.')
    parser.add_argument('-e', '--environment', required=True, metavar='environment', type=str, help='enter the environment: prod, dev, qa, preview')
    args = parser.parse_args()

    env = args.environment
    file = args.input_file

    s3_add_tags_prod(file, env)
    s3_add_tags_preview(file, env)
    s3_add_tags_dev(file, env)
    s3_add_tags_qa(file, env)


if __name__ == '__main__':
    main()