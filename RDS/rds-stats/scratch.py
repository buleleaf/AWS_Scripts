import sys
import boto3
import itertools
from collections import defaultdict

region = 'us-east-1'
# db_instance = 'db-instance-identifier'

rds = boto3.client('rds', region_name=region)

dbs = rds.describe_db_instances()

print dbs

# for db, db_status in dbs.iteritems():
#
#     for rds_status, info in db_status.iteritems():
#
#         for k, v in info.iteritems():
#             print k, v

# print(list(map(lambda x:list(map(lambda y:y['StorageType'],x)),dbs.values())))

# for kv in dbs.items():
#     print(kv)
#
# import boto3
#
# rds = boto3.client('rds')
#
# describe = rds.describe_db_instances()
#
# for kv in describe['DBInstances']
#     print (kv)

# import sys
# import boto3
#
# def main():
#     if len(sys.argv) < 2:
#         print("Please supply a VPC id as an argument!")
#     else:
#         vpc_id = sys.argv[1]
#         print("VPC ID:", vpc_id)
#
#         # Display RDS instances in VPC
#         client = boto3.client('rds')
#         response = client.describe_db_instances()
#
#         # Use Python lambda to filter DB instances that are in our VPC
#         rds_instances = list( filter( lambda x: x["DBSubnetGroup"]["VpcId"] == vpc_id, response["DBInstances"] ) )
#         if len(rds_instances) > 0:
#             print("\nRDS Instances:")
#             for rds in rds_instances:
#                 print(rds["Engine"])
#         else:
#             print("There is no RDS instance in this VPC!")
#
# if __name__ == "__main__":
#     main()
