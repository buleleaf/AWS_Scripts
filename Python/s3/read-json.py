import json
import boto3

def boto3_client(resource):
    """Create Boto3 client."""
    return boto3.client(resource)


def s3_add_tags(tags):
    boto3_client('s3').put_bucket_tagging(
        Bucket='dmansfield-dev',
        Tagging=tags
    )

def main():

    dev_tags_file = open('test.json')
    dev_tags = json.load(dev_tags_file)

    tags = dev_tags
    s3_add_tags(tags)


if __name__ == '__main__':
    main()