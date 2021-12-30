"""Creates an ASG, Target Group, Listeners, and Security Groups."""

from troposphere import (
    And, Equals, Export, FindInMap, Join, GetAtt, Sub, Tags, Not, Output, Ref, If,
    ec2, iam, AWSHelperFn
)
from troposphere import autoscaling as asg
from troposphere import elasticloadbalancingv2 as elbv2
from troposphere.policies import (
    UpdatePolicy, AutoScalingRollingUpdate
)
import awacs
import awacs.sts
from awacs.aws import (  # noqa: E0611
    Allow,
    Condition,
    Policy,
    Principal,
    Statement,
    StringEquals,
    StringLike,
)

from stacker.blueprints.base import Blueprint
from stacker.blueprints.variables.types import (
    CFNString, CFNCommaDelimitedList
)


class BlueprintClass(Blueprint):
    """Extend Stacker Blueprint class."""

    VARIABLES = {
        'CustomerName': {
            'type': CFNString,
            'description': 'The nickname for the customer/tenant. Must be all'
                           ' lowercase letters, should not contain spaces or '
                           'special characters, nor should it include any part'
                           ' of EnvironmentName',
            'allowed_pattern': '[-_ a-z]*',
            'default': 'undefined'
        },
        'ApplicationName': {
            'type': CFNString,
            'description': 'Instance name tag value (will have "CustomerName" '
                           'prepended and "EnvironmentName" appended to it)',
            'default': 'undefined'
        },
        'EnvironmentName': {
            'type': CFNString,
            'description': 'Name of Environment',
            'default': 'common'
        },
        'VpcId': {
            'type': CFNString,
            'description': 'VPC resources will be created in.'
        },
        'UserData': {
            'type': AWSHelperFn,
            'description': 'Instance user data',
            'default': Ref('AWS::NoValue')
        },        
        'bastionSubnetIds': {
            'type': CFNCommaDelimitedList,
            'description': 'Public subnets that the ASG will be created in.'
        },
        'bastionInstanceType': {
            'type': CFNString,
            'description': 'Type of the management instances',
            'default': 't3.small'
        },
        'bastionAsgMinValue': {
            'type': CFNString,
            'description': 'Minimum number of instances that will be running '
                           'in the autoscaling group',
            'default': '1'
        },
        'bastionAsgMaxValue': {
            'type': CFNString,
            'description': 'Maximum number of instances that will be running '
                           'in the autoscaling group',
            'default': '2'
        },
        'KeyName': {
            'type': CFNString,
            'description': 'Name of an existing EC2-VPC KeyPair',
            'default': ''
        },
        'AsgHealthCheckType': {
            'type': CFNString,
            'description': 'Autoscaling group Health Check type.',
            'default': 'EC2',
            'allowed_values': ['ELB', 'EC2']
        },
        'AttachedSgs': {
            'type': list,
            'description': 'List of Security Groups to have attached tothe instance'
        },
        'FromPort': {'type': CFNString,
                     'description': 'From Port',
                     'default': '22'
                     },
        'ToPort': {'type': CFNString,
                   'description': 'To Port',
                   'default': '22'
                   },
        'AMI': {'type': CFNString,
                   'description': 'Launch Config AMI',
                   },
    }

    def create_template(self):
        """Create template (main function called by Stacker)."""
        template = self.template
        variables = self.get_variables()

        template.add_mapping(
            'PaAmiRegionMap', {
                'us-east-1': {'AMI': 'ami-0c6b1d09930fac512'},  # (N. Virginia)
                'us-east-2': {'AMI': 'ami-0ebbf2179e615c338'},  # (Ohio)
                'us-west-1': {'AMI': 'ami-015954d5e5548d13b'},  # (N. California)
                'us-west-2': {'AMI': 'ami-0cb72367e98845d43'},  # (Oregon)
            }
        )

    # Instance Role
        instance_role = template.add_resource(
            iam.Role(
                'InstanceRole',
                AssumeRolePolicyDocument=Policy(
                    Version='2012-10-17',
                    Statement=[
                        Statement(
                            Effect=Allow,
                            Action=[
                                awacs.sts.AssumeRole
                            ],
                            Principal=Principal(
                                'Service',
                                [
                                    'ec2.amazonaws.com'
                                ]
                            )
                        ),
                    ]
                ),
                Path='/',
                ManagedPolicyArns=["arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore"],
                Policies=[
                    iam.Policy(
                        PolicyName=Join(
                            '-',
                            [
                                'private-bastion',
                                'role',
                                variables['EnvironmentName'].ref,
                                variables['CustomerName'].ref
                            ]
                        ),
                        PolicyDocument=Policy(
                            Version='2012-10-17',
                            Statement=[
                                Statement(
                                    Action=[
                                        awacs.aws.Action('ec2', 'AssociateAddress')
                                    ],
                                    Effect=Allow,
                                    Resource=['*']
                                ),
                                Statement(
                                    Action=[
                                        awacs.aws.Action('ssm','StartSession')
                                    ],
                                    Effect=Allow,
                                    Condition=Condition([
                                        StringLike(
                                        "ssm:resourceTag/Name", "prodly-common-bastion-host-private"
                                         ),
                                    ]),                                      
                                    Resource=['arn:aws:ec2:*:*:instance/*']
                                )
                            ]
                        )
                    ),
                ]
            )
        )

        template.add_output(
            Output(
                instance_role.title,
                Description='Logical ID of IAM role',
                Export=Export(
                    Sub('${AWS::StackName}-%s' % instance_role.title)
                ),
                Value=Ref(instance_role)
            )
        )

        template.add_output(
            Output(
                '%sARN' % instance_role.title,
                Description='ARN of IAM role',
                Export=Export(
                    Sub('${AWS::StackName}-%sARN' % instance_role.title)
                ),
                Value=GetAtt(instance_role, 'Arn')
            )
        )

        # Instance Profile
        instance_profile = template.add_resource(
            iam.InstanceProfile(
                'InstanceProfile',
                Path='/',
                Roles=[
                    Ref(instance_role)
                ]
            )
        )

        template.add_output(
            Output(
                instance_profile.title,
                Description='IAM Instance Profile',
                Export=Export(
                    Sub('${AWS::StackName}-%s' % instance_profile.title)
                ),
                Value=Ref(instance_profile)
            )
        )


    # Launch Configuration
        bastion_lc = template.add_resource(asg.LaunchConfiguration(
            'LaunchConfiguration',
            AssociatePublicIpAddress=False,
            IamInstanceProfile=Ref(instance_profile),
            ImageId=variables['AMI'].ref,
            InstanceType=variables['bastionInstanceType'].ref,
            InstanceMonitoring=True,
            KeyName=variables['KeyName'].ref,
            # SecurityGroups=variables['AttachedSgs'] + [Ref(bastionsercuritygroup)],
            SecurityGroups=variables['AttachedSgs'],
            UserData=variables['UserData'],
        ))

    # ASG
        bastion_asg = template.add_resource(asg.AutoScalingGroup(
            'bastionAsg',
            AutoScalingGroupName=Sub('${AWS::StackName}'),
            MinSize=variables['bastionAsgMinValue'].ref,
            MaxSize=variables['bastionAsgMaxValue'].ref,
            HealthCheckGracePeriod='600',
            HealthCheckType=variables['AsgHealthCheckType'].ref,
            LaunchConfigurationName=Ref(bastion_lc),
            Tags=[
                asg.Tag(
                    'Name',
                    Ref('AWS::StackName'),
                    True
                ),
                asg.Tag(
                    'Application',
                    variables['ApplicationName'].ref,
                    True
                ),
                asg.Tag(
                    'Environment',
                    variables['EnvironmentName'].ref,
                    True
                )
            ],
            VPCZoneIdentifier=variables['bastionSubnetIds'].ref
        ))
        template.add_output(Output(
            bastion_asg.title,
            Description='Name of autoscaling group',
            Value=Ref(bastion_asg),
        ))

# Helper section to enable easy blueprint -> template generation
# (just run `python <thisfile>` to output the json)
if __name__ == "__main__":
    from stacker.context import Context

    print(BlueprintClass('test', Context({'namespace': 'test'})).to_json({
        'VpcId': 'vpc-xxxx',
        'AlbSubnetIds': 'subnet-xxxx,subnet-yyyy',
        'TargetInstanceIds': ['i-xxxx'],
        'SecurityGroup': 'sg-xxxx'
    }))
