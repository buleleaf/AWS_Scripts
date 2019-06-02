import boto3

region = 'us-west-2'

info = []

client = boto3.client('ec2', region_name=region)
response = client.describe_network_interfaces()
for security_group in response['NetworkInterfaces']:
    for sg in security_group['Groups']:
        info.append(sg['GroupId'])
for network_interface in response['NetworkInterfaces']:
    info.append(network_interface['NetworkInterfaceId'])



info.sort()
print(info)


# def get_

# def main():
#     region = 'us-west-2'
#     network_int = set()
#     get_network_interfaces(region, network_int)
#     network_interfaces = get_network_interfaces(region, network_int)
#     for sg in network_interfaces:
#         print(sg)


# if __name__== "__main__":
#     main()