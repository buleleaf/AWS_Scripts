import boto3
import os
os.environ['AWS_DEFAULT_REGION'] = 'us-east-1'

class ManagedInstances():
    def __init__(self):
        self.ec2 = boto3.client('ec2')
        self.ssm = boto3.client('ssm')
    def describe_instances(self):
        for page in self.ec2.get_paginator('describe_instances').paginate():
            for reservation in page['Reservations']:
                for instance in reservation['Instances']:
                    yield instance
    def describe_instance_information(self):
        for page in self.ssm.get_paginator('describe_instance_information').paginate():
            for instance in page['InstanceInformationList']:
                yield instance
    def ec2_instances(self):
        return set([i['InstanceId'] for i in self.describe_instances()])
    def ssm_instances(self):
        return set([i['InstanceId'] for i in self.describe_instance_information()])
    def compare(self, src, comp):
        return src - comp


def main():
    client = ManagedInstances()
    ssm_instances = client.ssm_instances()
    ec2_instances = client.ec2_instances()
    unmanaged_instances = client.compare(ec2_instances, ssm_instances)

    print('Unmanaged Instance count: {}'.format(len(unmanaged_instances)))
    print('Managed Instance count: {}'.format(len(ssm_instances)))
    print('EC2 Instance count: {}'.format(len(ec2_instances)))
    if unmanaged_instances:
        print('Unmanaged Instances:')
        print('\n'.join(list(unmanaged_instances)))

if __name__ == '__main__':
    main()
