# pip install boto3

import boto3

#Instance Specifications
license_model = 'license-included'
#Oracle
db_engine = 'oracle-se2'
db_engine_version = '12.1.0.2.v16'

db_instance_class = 'db.t2.medium'
availability_zone = 'us-west-2a'
multi_az = False

storage_type = 'GP2'
allocated_storage = 100
storage_autoscaling = True
max_storage_size = 1000

db_instance_idenfifier = 'AWOR-DVRDSORA04'

master_username = 'admin'
master_password = 'B57M383J9RFlAuROmQ3H'


# Network & Security

db_subnet_group_name = 'vpcnasharedservices-protected'
publicy_accessible = False
# VPC Shared Services
sg_1 = 'sg-85375fe3'
sg_2 = 'sg-f7262991'
sg_3 = 'sg-c00961a6'
sg_4 = 'sg-ed08608b'


# Database Options

database_name ='EUMCMPD'
# Oracle
port = 1521
db_paramater_group = 'default.oracle-se2-12.1'
option_group = 'default:oracle-se2-12-1'
character_set_name = 'AL32UTF8'


rds_client = boto3.client('rds', region_name='us-west-2')

rds_instance = rds_client.create_db_instance(
    AvailabilityZone=availability_zone,
    AutoMinorVersionUpgrade=False,
    CopyTagsToSnapshot=True,
    DeletionProtection=False,
    MultiAZ=multi_az,
    PubliclyAccessible=publicly_accessible,
    StorageEncrypted=True,
    AllocatedStorage=allocated_storage,
    BackupRetentionPeriod=7,
    Iops=0,
    MonitoringInterval=0,
    Port=port,
    DBInstanceClass=db_instance_class,
    DBInstanceIdentifier=db_instance_identifier,
    DBName=db_name,
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
    SupportsStorageAutoscaling=storage_autoscaling,
    MaxStorageSize=max_storage_size,
    VPCSecurityGroupIds= [
        sg_1,
        sg_2,
        sg_3,
        sg_4
    ],
    Tags= [
        {
            "Key": "Application",
            "Value": "Oracle"
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
            "Value": "Yes"
        },
        {
            "Key": "Environment",
            "Value": "Development"
        },
        {
            "Key": "Name",
            "Value": "AWOR-DVRDSORA04"
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
            "Value":"SNOW Ticket"
        },
        {
            "Key": "OperationalHours",
            "Value": "24x7"
        },
        {
            "Key": "ReviewDate",
            "Value": "6/20/2019"
        },
        {
            "Key": "CostCenter",
            "Value": "1001596013"
        },
        {
            "Key": "ServiceLocation",
            "Value": "Irvine"
        },
        {
            "Key": "ServiceOwner",
            "Value": "Amir Memaran/Mike Lockwood"
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
            "Value": "PilotAutoReboot"
        },
        {
            "Key": "Schedule",
            "Value": "24x7"
        },
        {
            "Key": "Purpose",
            "Value": "Windchill 11.2 Sandbox System"
        },
        {
            "Key": "Validated",
            "Value": "No"
        }
    ]
)