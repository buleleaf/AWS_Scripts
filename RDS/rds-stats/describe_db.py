import sys
import boto3
from collections import defaultdict

region = 'us-east-1'
# db_instance = 'db-instance-identifier'

rds = boto3.client('rds', region_name=region)

dbs = rds.describe_db_instances()

print(dbs['DBInstances'])

# rdsinfo = defaultdict()
# for db in dbs['DBInstances']:
#     rdsinfo[db.id] = {
#         'Tag': db.DBInstances,
#         # 'Type': db.DBInstanceClass,
#         # 'State': db.Engine,
#         # 'Private IP': db.DBInstanceStatus,
#         # 'Public IP': db.MasterUsername,
#         # 'Launch Time': db.DBName
#         }
#
# attributes = ['Tag', 'Type', 'Private IP', 'Public IP', 'Launch Time', 'State']
# for db_id, db in ec2info.items():
#     for key in attributes:
#         print("{0}: {1}".format(key, db[key]))
#     print("-------------------------")

# for kv in dbs.items():
#     print(kv[1])

# print(dbs.keys())


# for k, v in dbs.items():
#     print(k, v, "\n")
#

# #
# for db in dbs['DBInstances']:
#     print ("%s@%s:%s %s") % (
#     db['MasterUsername'],
#     db['Endpoint']['Address'],
#     db['Endpoint']['Port'],
#     db['DBInstanceStatus'])
# #


sys.exit()
# db['Endpoint']['Address'],
# db['Endpoint']['Port'],
# db['DBInstanceStatus'])
#
#
# for db in dbs['DBInstances']:
#     print ("%s@%s:%s %s") % (


# print(response)


#
# def lambda_handler(event, context):
#     source = boto3.client('rds', region_name=region)
#     try:
#         instances = source.describe_db_instances(DBInstanceIdentifier=db_instance)
#         rds_host = instances.get('DBInstances')[0].get('Endpoint').get('Address')
#     except Exception as e:
#         raise e



        # or
        # rds_host = instances.get('DBInstances')[0]['Endpoint']['Address']
