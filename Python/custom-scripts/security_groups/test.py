import os

sg1 = "sg-0964887a556e1b9ff"
sg2 = "sg-0e42e8154106ab899"
sg3 = "sg-04b98dd0a613e4873"
sg4 = "sg-034aef491d100e6a1"
sg5 = "sg-0d778ff6c38911f20"

os.system("aws ec2 delete-security-group --group-id {}".format(sg1))
os.system("aws ec2 delete-security-group --group-id {}".format(sg2))
os.system("aws ec2 delete-security-group --group-id {}".format(sg3))
os.system("aws ec2 delete-security-group --group-id {}".format(sg4))
os.system("aws ec2 delete-security-group --group-id {}".format(sg5))