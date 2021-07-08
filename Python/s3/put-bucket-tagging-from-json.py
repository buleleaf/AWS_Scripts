#!/usr/bin/env python3
import boto3
import argparse
import csv
import botocore

# parse command line argumetns
def parse_args():
    parser = argparse.ArgumentParser(prog='csv-to-tags', description='Append tags to S3 Buckets from a CSV file.')
    # required
    parser.add_argument('-i', '--in', required=True, action='store', dest='input_file', type=str, help='path to where the input file is located.')

    # optional
    parser.add_argument('-r', '--region',action='store', default='us-east-2', dest='aws_region', type=str, help='AWS region to use.')
    parser.add_argument('-v', '--version', action='version', version='0.1')

    args = parser.parse_args()
    return args

def s3_list_buckets():
    s3_bucket = s3.list_buckets()
    for buckets in s3_bucket['Buckets']:
        yield buckets['Name']

# def append_buckets():
#     bucket_list = []
#     for bucket in s3_list_buckets():
#         bucket_list.append(bucket)
#     return [b for b in bucket_list]


# def tags_from_row(row, columns):
#     tags = []
#     for c in range(1, len(row)):
#         tag = {}
#         tag['Key'] = columns[c]
#         tag['Value'] = row[c]
#         tags.append(tag)
#     return tags

# def append_tags(s3_bucket, tags):
#     if s3_bucket and tags:
#         try:
#             response = s3.put_bucket_tagging(
#                 Bucket=[s3_bucket],
#                 Tagging={
#                     'TagSet': tags
#                 }
#             )
#         except botocore.exceptions.ClientError as e:
#             print(e.response['Error']['Message'])



# def get_bucket_tagging():
#     for buckets in s3_list_buckets():
#         try:
#             print(buckets)
#             s3.get_bucket_tagging(Bucket=buckets)
#         except ClientError:
#             print(f"S3 bucket {buckets} does not have tags.")


def main():

    global args
    global s3

    args = parse_args()
    
    s3 = boto3.client('s3', region_name=args.aws_region)

    s3_bucket = s3_list_buckets()

    if s3_bucket:
        try:
            print(s3_bucket)
            s3.get_bucket_tagging(Bucket=s3_bucket)
        except botocore.exceptions.ClientError:
            print(f"S3 bucket {s3_bucket} does not have tags.")


    # s3_bucket = []

    # for bucket in s3_list_buckets():
    #     s3_bucket.append(bucket)

    # print(s3_bucket)

    # for bucket in s3_list_buckets():
    #     print(bucket)




    # with open(args.input_file, 'rt') as csvfile:
    #     reader = csv.reader(csvfile, delimiter=',')
    #     tag_names = []
    #     rows = list(reader)
    #     columns = rows[0]
    #     for r in range(1, len(rows)):
    #         tags = tags_from_row(rows[r], columns)
    #         append_tags(s3_bucket, tags)

# for bucket in s3.buckets.all():
#     s3_bucket = bucket
#     s3_bucket_name = s3_bucket.name
#     try:
#         response = s3_client.get_bucket_tagging(Bucket=s3_bucket_name)
#         #print response
#         #tagset = response['TagSet']
#     except ClientError:
#         print s3_bucket_name, "does not have tags, adding tags"




#     bucket_list = set()
#     s3_list_buckets(bucket_list)
#     # print(bucket_list)
#     for buckets in bucket_list:
#         boto3_client('s3').get_bucket_tagging(Bucket=buckets)
#     print(buckets)
    # tags = boto3_client('s3').get_bucket_tagging(Bucket='dmansfield-test-bucket')

if __name__ == '__main__':
    main()