#!/usr/bin/env python3
import boto3
import botocore
import functools
import json

@functools.lru_cache()
def boto3_client(resource):
    """Create Boto3 client."""
    return boto3.client(resource)


def s3_list_buckets():
    s3_bucket = boto3_client('s3').list_buckets()
    for buckets in s3_bucket['Buckets']:
        yield buckets['Name']

def s3_add_tags(tags):
    for buckets in s3_list_buckets():
        boto3_client('s3').put_bucket_tagging(
            Bucket=buckets,
            Tagging={
                'TagSet': [tags]
            }
        )

def get_bucket_tagging():
    for buckets in s3_list_buckets():
        try:
            print(buckets)
            boto3_client('s3').get_bucket_tagging(Bucket=buckets)
        except botocore.exceptions.ClientError:
            print(f"S3 bucket {buckets} does not have tags.")


def main():
    f = open('tag.json')
    tags = json.load(f)
    s3_add_tags(tags)
    get_bucket_tagging()
    # s3_bucket = s3_list_buckets()

    # for bucket in s3_bucket:
    #     print(bucket)


    f.close()

if __name__ == '__main__':
    main()