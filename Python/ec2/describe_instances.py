import boto3

def list_instances_by_tag_value(tagkey, tagvalue):
    # When passed a tag key, tag value this will return a list of InstanceIds that were found.

    ec2client = boto3.client('ec2')

    response = ec2client.describe_instances(
        Filters=[
            {
                'Name': 'tag:'+tagkey,
                'Values': [tagvalue]
            }
        ]
    )
    instancelist = []
    for reservation in (response["Reservations"]):
        for instance in reservation["Instances"]:
            instancelist.append(instance["InstanceId"])
    return instancelist
