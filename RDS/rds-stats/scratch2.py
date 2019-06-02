import boto3

region = 'us-east-1'
# db_instance = 'db-instance-identifier'

rds = boto3.client('rds', region_name=region)

dbs = rds.describe_db_instances()

for output in dbs['DBInstances']:
    print('Master Username: ' + output['MasterUsername'] +
    '\nBackup Window: ' + output['PreferredBackupWindow'])

# print ([rds['MasterUsername'] for rds in dbs['DBInstances']])
