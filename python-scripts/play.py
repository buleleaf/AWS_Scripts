#!/usr/bin/env python
# Ver. 1.0.1


import boto3
from pprint import pprint
import itertools

TAG_KEYS = 'Name', 'Env', 'Appname'

# Add credentials below
session = boto3.Session()
ec2 = session.resource('ec2')

instances = []
for instance in ec2.instances.all():
    instances.append(instance.tags)
clean = filter(None,instances)
flat_list = list(itertools.chain.from_iterable(clean))
value_list = []
for instances in flat_list:
    value_list.append(instances['Value'])
results = set(value_list)
print("{0:20}   {1}".format("\nCount","Value\n"))
for values in results:
    if values == "":
        print('{0:20}   {1}'.format("**BLANK VALUE**", value_list.count(values)))
    else:
        print('{0:20}   {1}'.format(values, value_list.count(values)))
print("\n")
