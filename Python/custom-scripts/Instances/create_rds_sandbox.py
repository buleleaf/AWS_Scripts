import random
import string
import boto3

def passwordGenerator(stringLength=20):
    """ Generates a random string of fixed length"""
    password_characters = string.ascii_letters + string.digits
    return ''.join(random.choice(password_characters) for i in range(stringLength))

# DATABASE INSTANCE SPECIFICATIONS
#Database Name
db_instance_name = 'test-rds'

#Credentials
master_username = 'admin'
master_password = passwordGenerator(20)

#Software
license_model = 'license-included'

#Oracle
db_engine = 'oracle-se2'
db_engine_version = '12.1.0.2.v16'

#Hardware
db_instance_class = 'db.t2.micro'

# Storage
storage_type = 'GP2'
allocated_storage = 200
max_storage_size = 1000

# NETWORK AND SECURITY
db_subnet_group_name = 'default'
publicy_accessible = False
availability_zone = 'us-west-2a'
multi_az = False
# VPC Shared Services Security Groups
sg_1 = 'default' # lab default
# sg_1 = 'sg-85375fe3' # SG-SS-MGMT-ALLTRAFFIC-OUT
# sg_2 = 'sg-f7262991' # SG-SS-TIER-PROTECTED
# sg_3 = 'sg-c00961a6' # SG-SS-MGMT-RDPSSH-IN
# sg_4 = 'sg-ed08608b' # SG-SS-MGMT-CORESERVICES


# DATABASE OPTIONS
database_name ='lab'
# Oracle
port = 1521
db_paramater_group = 'default.oracle-se2-12.1'
option_group = 'default:oracle-se2-12-1'
character_set_name = 'AL32UTF8'

print("RDS Instance has been created with a random Master Password.")
print(f"Please give this to the customer via LastPass: {passwordGenerator(20)}")

rds_client = boto3.client('rds', region_name='us-west-2')

rds_instance = rds_client.create_db_instance(
    AvailabilityZone=availability_zone,
    AutoMinorVersionUpgrade=False,
    CopyTagsToSnapshot=True,
    # DeletionProtection=False,
    MultiAZ=multi_az,
    PubliclyAccessible=False,
    # StorageEncrypted=True,
    AllocatedStorage=allocated_storage,
    BackupRetentionPeriod=7,
    Iops=0,
    MonitoringInterval=0,
    Port=port,
    DBInstanceClass=db_instance_class,
    DBInstanceIdentifier=db_instance_name,
    DBName=database_name,
    DBParameterGroupName=db_paramater_group,
    DBSubnetGroupName=db_subnet_group_name,
    Engine=db_engine,
    EngineVersion=db_engine_version,
    LicenseModel=license_model,
    MasterUserPassword=master_password,
    MasterUsername=master_username,
    OptionGroupName=option_group,
    StorageType=storage_type,
    CharacterSetName=character_set_name,
    # MaxAllocatedStorage=max_storage_size,
    # VpcSecurityGroupIds= [
    #     sg_1,
        # sg_2,
        # sg_3,
        # sg_4
    # ],
    Tags= [
        {
            "Key": "Application",
            "Value": "Database server for EU material compliance database for MDR project"
        },
        {
            "Key": "ApplicationTier",
            "Value": "Database"
        },
        {
            "Key": "ApplicationTierLevel",
            "Value": "No Tier"
        },
        {
            "Key": "Managed",
            "Value": "No"
        },
        {
            "Key": "Environment",
            "Value": "Production"
        },
        {
            "Key": "Name",
            "Value": db_instance_name
        },
        {
            "Key": "CorpInfoMSP:TakeNightlySnapshot",
            "Value": "No"
        },
        {
            "Key": "FileLevelBackup",
            "Value": "No"
        },
        {
            "Key": "MonitoredServices",
            "Value": "No"
        },
        {
            "Key":"RequestNumber",
            "Value":"RITM0031702"
        },
        {
            "Key": "OperationalHours",
            "Value": "24x7"
        },
        {
            "Key": "ReviewDate",
            "Value": "6/26/2019"
        },
        {
            "Key": "CostCenter",
            "Value": "Christine Crawford Cost center 1001798953 subledger 61827869"
        },
        {
            "Key": "ServiceLocation",
            "Value": "Irvine"
        },
        {
            "Key": "ServiceOwner",
            "Value": "Alek Slavuk"
        },
        {
            "Key": "TechnicalOwner",
            "Value": "Alek Slavuk/Haihao Li"
        },
        {
            "Key": "ContactPreference",
            "Value": "Email"
        },
        {
            "Key": "PatchGroup",
            "Value": "ProductionManualReboot"
        },
        {
            "Key": "Schedule",
            "Value": "24x7"
        },
        {
            "Key": "Purpose",
            "Value": "Database server for EU material compliance database for MDR project"
        },
        {
            "Key": "Validated",
            "Value": "No"
        }
    ]
)