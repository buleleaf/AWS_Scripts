from collections import defaultdict
import boto3
ec2 = boto3.resource('ec2')
ec2_filter = [{'Name': 'instance-state-name', 'Values': ['stopped']}]

ec2.instances.filter(Filters=ec2_filter).start()

instance_status = ec2.instances.filter(Filters=[{
    'Name': 'instance-state-name',
    'Values': ['running', 'pending']}])

ec2info = defaultdict()
for instance in instance_status:
    ec2info[instance.id] = {
        'Type': instance.instance_type,
        'ID': instance.id,
        'State': instance.state['Name'],
        'Private IP': instance.private_ip_address,
        }

attributes = ['Type', 'ID', 'State', 'Private IP']
for instance_id, instance in ec2info.items():
    for key in attributes:
        print("{0}: {1}".format(key, instance[key]))
    print("-------------------------")
