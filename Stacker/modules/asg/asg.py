#!/usr/bin/env python
"""Stacker module for creating a standalone ASG."""
from utils import standalone_output

from troposphere import (
    And, Equals, If, Join, Not, Output, Ref, Sub, autoscaling, ec2, iam, AWSHelperFn, NoValue
)
from troposphere.autoscaling import MetricsCollection
from troposphere.policies import (
    UpdatePolicy, AutoScalingRollingUpdate  # , AutoScalingReplacingUpdate
)

from stacker.blueprints.base import Blueprint

import awacs.ec2
import awacs.s3
import awacs.ssm
import awacs.sts
import json
from awacs.aws import Allow, Policy, Principal, Statement
# Linter is incorrectly flagging the automatically generated functions in awacs
from awacs.aws import StringEquals, StringLike  # noqa pylint: disable=no-name-in-module


from stacker.blueprints.variables.types import (
    CFNCommaDelimitedList, CFNNumber, CFNString, EC2SecurityGroupIdList,
    EC2SubnetIdList
)


class Asg(Blueprint):
    """Extend Stacker Blueprint class."""

    VARIABLES = {
        'AppAMI': {
            'type': CFNString,  # Not EC2ImageId to allow blank value
            'description': 'AMI ID for app instances; leave blank to '
                           'automatically look up the via "AMILookupArn".',
            'default': '',
        },
        'AppInstanceType': {
            'type': CFNString,
            'description': 'Type of the instances',
            'default': 't2.small',
        },
        'AppPolicies': {
            'type': CFNCommaDelimitedList,
            'description': 'IAM managed policy ARNs to apply to the instances',
        },
        'AppSecurityGroups': {
            'type': EC2SecurityGroupIdList,
            'description': 'Security groups to apply to the instances',
        },
        'AppSubnets': {
            'type': EC2SubnetIdList,
            'description': 'Subnets in which the app server(s) will be'
                           ' deployed',
        },
        'Application': {
            'type': CFNString,
            'description': 'Instance name tag value (will have "Company" '
                           'prepended and "EnvironmentName" appended to it)',
            'default': 'application',
        },
        'ASGMinValue': {
            'type': CFNString,
            'description': 'Minimum number of instances that will be running '
                           'in the autoscaling group',
            'default': '1',
        },
        'ASGAutoDeploy': {
            'type': CFNString,
            'description':  'Auto Scaling Rolling Update Policy specifies'
                            'how CloudFormation handles rolling updates.',
            'default': 'true',
            'allowed_values':   [
                'true',
                'false',
            ],
        },
        'ASGMaxValue': {
            'type': CFNString,
            'description': 'Maximum number of instances that will be running '
                           'in the autoscaling group',
            'default': '1',
        },
        'AsgPauseTime': {
            'type': CFNString,
            'description': 'How long before nuking the next instance',
            'default': 'PT7M',
        },
        'UserData': {
            'type': AWSHelperFn,
            'description': 'Instance user data',
            'default': Ref('AWS::NoValue'),
        },
        'Backup': {
            'type': CFNString,
            'description': 'Backup',
            'default': False,
        },
        'BackupHourly': {
            'type': CFNString,
            'description': 'Hourly Backup',
            'default': False,
        },
        'Company': {
            'type': CFNString,
            'description': 'The nickname for the customer/tenant. Must be all'
                           ' lowercase letters, should not contain spaces or '
                           'special characters, nor should it include any part'
                           ' of EnvironmentName',
            'allowed_pattern': '[-_ a-z]*',
            'default': 'doctor-genius',
        },
        # 'CostCenter': {
        #     'type': CFNString,
        #     'description': 'CostCenter',
        # },
        'Creator': {
            'type': CFNString,
            'description': 'Creator',
            'default': '',
        },
        'CwLogFilter': {
            'type': CFNString,
            'description': 'Creator',
            'default': '',
        },
        # 'DataClassification': {
        #     'type': CFNString,
        #     'description': 'DataClassification',
        # },
        'Environment': {
            'default': 'dev',
            'type': CFNString,
            'description': 'Name of Environment',

        },
        'StatelessHaEnabled': {
            'type':CFNString,
            'description': 'Flag to enable snowblower',
            'default': 'no',
            'allowed_values':   [
                'yes',
                'no',
            ],
        },
        'HealthCheckGracePeriod': {
            'type': CFNNumber,
            'description': 'ASG health check grace period (in seconds)',
            'default': '600'
        },
        'HealthCheckType': {
            'type': CFNString,
            'description': 'Type of ASG health check',
            'default': 'EC2',
            'allowed_values': [
                'EC2',
                'ELB'
            ]
        },
        'KeyName': {
            'type': CFNString,
            'description': 'Name of an existing EC2-VPC KeyPair',
            'default': ''
        },
        'ScalingSnsTopic': {
            'type': CFNString,
            'description': 'SnsTopic to send scaling notifications to',
            'default': ''
        },
        'MetricsCollection': {
            'type': CFNString,
            'description': 'Should the autoscaling have metrics?',
            'default': 'true',
            'allowed_values': [
                'true',
                'false'
            ]
        },
        'MetricsCollectionGranularity': {
            'type': CFNString,
            'description': 'How often to pull metrics',
            'default': '1Minute'
        },
        'Role': {
            'type': CFNString,
            'description': 'Role tag',
            'default': ''
        },
        'Service': {
            'type': CFNString,
            'description': 'Service tag',
            'default': ''
        },
        'TargetGroupARNs': {
            'type': CFNCommaDelimitedList,
            'description': 'Target Group list',
        },
        # 'TechOwner': {
        #     'type': CFNString,
        #     'description': 'Tech Owner',
        # },
        'TechOwnerEmail': {
            'type': CFNString,
            'description': 'Tech Owner Email',
        },
        'MinInstancesInService': {
            'type': CFNString,
            'description': 'Minimum Instances In Service for ASG UpdatePolicy',
            'default': '1'
        },
        'MSBuildConfiguration': {
            'type': CFNString,
            'description': 'MSBuildConfiguration Tag',
        },
    }

    def add_resources(self):
        """Add ASG to template."""
        template = self.template
        variables = self.get_variables()

        role_policy_statements = [
            Statement(
                Action=[awacs.aws.Action('elasticloadbalancing', '*')],
                Effect=Allow,
                Resource=['*']
            ),
            Statement(
                Action=[
                    awacs.ssm.GetParameter,
                    awacs.ec2.DescribeInstances,
                ],
                Effect=Allow,
                Resource=["*"]
            ),

        ]


        targetgrouparnsomitted = 'TargetGroupARNsOmitted'
        template.add_condition(
            targetgrouparnsomitted,
            Equals(Join('', variables['TargetGroupARNs'].ref), '')
        )

        # Resources
        server_role = template.add_resource(
            iam.Role(
                'ServerServerRole',
                AssumeRolePolicyDocument=Policy(
                    Version='2012-10-17',
                    Statement=[
                        Statement(
                            Effect=Allow,
                            Action=[awacs.sts.AssumeRole],
                            Principal=Principal('Service',
                                                ['ec2.amazonaws.com'])
                        )
                    ]
                ),
                ManagedPolicyArns=variables['AppPolicies'].ref,
                Path='/',
                Policies=[
                    iam.Policy(
                        PolicyName=Join('-',
                                        [variables['Company'].ref,
                                         variables['Application'].ref,
                                         'app-role',
                                         variables['Environment'].ref]),
                        PolicyDocument=Policy(
                            Version='2012-10-17',
                            Statement=role_policy_statements
                        )
                    ),

                ]
            )
        )

        server_profile = template.add_resource(
            iam.InstanceProfile(
                'ServerInstanceProfile',
                Path='/',
                Roles=[Ref(server_role)]
            )
        )

        server_launch_config = template.add_resource(
            autoscaling.LaunchConfiguration(
                'LaunchConfig',
                IamInstanceProfile=Ref(server_profile),
                ImageId=variables['AppAMI'].ref,
                InstanceType=variables['AppInstanceType'].ref,
                InstanceMonitoring=True,
                KeyName=variables['KeyName'].ref,
                SecurityGroups=variables['AppSecurityGroups'].ref,
                UserData=variables['UserData']
            )
        )
        asg_tags = [
            autoscaling.Tag(
                'Name',
                Join('-', [variables['Company'].ref,
                           variables['Application'].ref,
                           variables['Role'].ref,
                           variables['Environment'].ref]), True
            ),
            autoscaling.Tag('Application',
                            variables['Application'].ref, True),
            autoscaling.Tag('AutoAlarmCreation', 'True', True),
            autoscaling.Tag('Company',
                            variables['Company'].ref, True),
            autoscaling.Tag('Environment',
                            variables['Environment'].ref, True),
            # autoscaling.Tag('TechOwner',
            #                 variables['TechOwner'].ref, True),
            autoscaling.Tag('TechOwnerEmail',
                            variables['TechOwnerEmail'].ref, True),
            autoscaling.Tag('Backup',
                            variables['Backup'].ref, True),
            autoscaling.Tag('BackupHourly',
                            variables['BackupHourly'].ref, True),
            # autoscaling.Tag('DataClassification',
            #                 variables['DataClassification'].ref, True),
            autoscaling.Tag('StatelessHa',
                            variables['StatelessHaEnabled'].ref, True),
            autoscaling.Tag('MSBuildConfiguration',
                            variables['MSBuildConfiguration'].ref, True),
        ]
        optional_tags = ['Role', 'Service']
        for tag in optional_tags:
            if variables[tag].value != '':
                asg_tags.append(
                    autoscaling.Tag(tag, variables[tag].ref, True)
                )

        auto_deploy = variables['ASGAutoDeploy'].value
        if auto_deploy == 'true':
            update_policy = UpdatePolicy(
                AutoScalingRollingUpdate=AutoScalingRollingUpdate(
                    PauseTime=variables['AsgPauseTime'].ref,
                    MinInstancesInService=variables['MinInstancesInService'].ref,
                    MaxBatchSize='1',
                )
            )

        else:
            update_policy = UpdatePolicy(AutoScalingRollingUpdate=NoValue)


        server_asg = template.add_resource(
            
            autoscaling.AutoScalingGroup(
                'AutoScaleGroup',
                AutoScalingGroupName = Join('-', [variables['Company'].ref,
                           variables['Application'].ref,
                           variables['Role'].ref,
                           variables['Environment'].ref]),
                UpdatePolicy = update_policy,
                MinSize=variables['ASGMinValue'].ref,
                MaxSize=variables['ASGMaxValue'].ref,
                HealthCheckGracePeriod=variables['HealthCheckGracePeriod'].ref,
                HealthCheckType=variables['HealthCheckType'].ref,
                MetricsCollection=[autoscaling.MetricsCollection(
                    Granularity='1Minute'
                )],
                LaunchConfigurationName=Ref(server_launch_config),
                Tags=asg_tags,
                TargetGroupARNs=If(
                    targetgrouparnsomitted,
                    Ref('AWS::NoValue'),
                    variables['TargetGroupARNs'].ref
                ),
                VPCZoneIdentifier=variables['AppSubnets'].ref
            )
        )

        template.add_output(Output(
            'ASG',
            Description='Name of autoscaling group',
            Value=Ref(server_asg),
        ))

    def create_template(self):
        """Create template (main function called by Stacker)."""
        template = self.template
        variables = self.get_variables()
        template.add_version('2010-09-09')
        template.add_description("Onica - ASG [App: %s Role: %s]- (1.0.0)" %
                                 (variables['Application'].value,
                                  variables['Role'].value))
        self.add_resources()


# Helper section to enable easy blueprint -> template generation
# (just run `python <thisfile>` to output the json)
if __name__ == "__main__":
    from stacker.context import Context

    standalone_output.json(
        blueprint=Asg('test',
                      Context({"namespace": "test"}),
                      None)
    )