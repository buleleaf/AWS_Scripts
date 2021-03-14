import os

# sg1 = "sg-00172d67"
# sg2 = "sg-00379879"
# sg3 = "sg-01e1e4e05785e22b0"
# sg4 = "sg-0212b965"
# sg5 = "sg-02415f874f0bcdb3b"

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


# os.system("aws ec2 delete-security-group --group-id {}".format(sg2))
# os.system("aws ec2 delete-security-group --group-id {}".format(sg3))
# os.system("aws ec2 delete-security-group --group-id {}".format(sg4))
# os.system("aws ec2 delete-security-group --group-id {}".format(sg5))
