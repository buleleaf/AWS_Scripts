import boto3
import csv
import json

def get_security_groupId(region):
    sgId = set()
    client = boto3.client('ec2', region_name=region)
    resp = client.describe_security_groups()
    for sg in resp['SecurityGroups']:
        sgId.add(sg['GroupId'])
    return sgId


def main():
    region = 'us-west-2'
    sgId = set()
    security_groupId = get_security_groupId(region)
    for sgId in security_groupId:
        print(sgId)
    with open('sadsa.csv', 'w') as outfile:
        json.dump(list(security_groups), outfile)

if __name__== "__main__":
    main()