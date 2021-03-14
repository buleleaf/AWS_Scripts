import boto3
​
​
def get_ec2_instances(region, used_sgs):
    ec2client = boto3.client('ec2', region_name=region)
    resp = ec2client.describe_instances()
    for reservation in resp['Reservations']:
        for instance in reservation['Instances']:
            for sg in instance['SecurityGroups']:
                used_sgs.add(sg['GroupId'])
​
​
def get_rds_instance(region, used_sgs):
    rdsclient = boto3.client('rds', region_name=region)
    resp = rdsclient.describe_db_security_groups()
    for dbsg in resp['DBSecurityGroups']:
        for sg in dbsg['EC2SecurityGroups']:
            used_sgs.add(sg['EC2SecurityGroupId'])
​
​
def get_elb_instance(region, used_sgs):
    client = boto3.client('elb')
    resp = client.describe_load_balancers()
    for lb in resp['LoadBalancerDescriptions']:
        for sg in lb['SecurityGroups']:
            used_sgs.add(sg)
​
​
def get_security_groups(region):
    sgs = set()
    client = boto3.client('ec2', region_name=region)
    resp = client.describe_security_groups()
    for sg in resp['SecurityGroups']:
        sgs.add(sg['GroupId'])
    return sgs
​
def main():
    region = 'us-west-2'
    used_sgs = set()
    get_ec2_instances(region, used_sgs)
    get_rds_instance(region, used_sgs)
    get_elb_instance(region, used_sgs)
    security_groups = get_security_groups(region)
    unused_security_groups = security_groups.difference(used_sgs)
    for sg in unused_security_groups:
        print(sg)