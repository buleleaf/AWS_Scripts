import os

security_groups = [
'sg-0b645bfe7bd38b1a0',
'sg-0e82326c679df95a0',
'sg-0ac8caa60501d001e',
'sg-08aefb3dc5636f542',
'sg-01d7e6d8bc8aa167e',
'sg-02f655b24dd906a5d',
'sg-0b32338d91d18d8e1',
    ]

for sg in security_groups:
    os.system("aws ec2 delete-security-group --group-id {}".format(sg))