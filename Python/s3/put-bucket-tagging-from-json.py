#!/usr/bin/env python3
import boto3
import functools
import os
import argparse
import pprint

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Create tags to S3 buckets from a JSON file.')
    parser.add_argument('-i', '--in', required=True, action='store', dest='input_file', type=str, help='path to where the input file is located.')
    return vars(parser.parse_args())


@functools.lru_cache()
def boto3_client(resource):
    """Create Boto3 client for S3."""
    return boto3.client(resource)


def s3_list_buckets(bucket_list):
    s3_bucket = boto3_client('s3').list_buckets()
    for bucket_list in s3_bucket['Buckets']:
        if (bucket_list['Name']):
            bucket_list.add(bucket_list['Name'])
    return bucket_list



# def s3_bucket_names():
#     for bucket in s3_list_buckets():
#         # for name in bucket['Name']:
#         #     return name
#         # yield bucket
#         yield bucket


# def s3_put_bucket_tagging():
#     bucket = s3_list_buckets()
#     self.__client.put_bucket_tagging(
#         Bucket=bucket,
#         Tagging={
#             'TagSet': [

#             ]
#         }
#     )

# def s3_bucket_names(buckets):
#     for bucket in buckets:
#         yield [b for b in bucket['Name']]


def s3_get_bucket_policy():
    bucket_list = set()
    s3_list_buckets(bucket_list)
    for bucket in bucket_list:
        for b in bucket:
            return boto3_client('s3').get_bucket_policy(Bucket=[b])


def main():
    # s3_list_buckets()
    # bucket = s3_get_bucket_policy()
    bucket = s3_get_bucket_policy()
    print(bucket)
    # for b in bucket:
    #     print(b)


if __name__ == '__main__':
    main()