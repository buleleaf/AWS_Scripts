""" Load dependencies """
from utils import standalone_output

from troposphere import (
    Export, Output, Ref, Sub, ec2, Not, Equals
)

from stacker.blueprints.base import Blueprint
from stacker.blueprints.variables.types import (
    CFNString
)


class SecurityGroupsIngress(Blueprint):
    """ Blueprint for Sturdy Networks ELB security groups """

    VARIABLES = {
        'FromPort': {'type': CFNString,
                     'description': 'From Port',
                     'default': '22'},
        'ToPort': {'type': CFNString,
                   'description': 'To Port',
                   'default': '22'},
        'IpProtocol': {'type': CFNString,
                       'description': 'Protocol',
                       'default': 'tcp'},
        'CidrIp': {'type': CFNString,
                   'description': 'CidrIp for Client',
                   'default': ''},
        'GroupId': {'type': CFNString,
                    'description': 'Security Group to add rule',
                    'default': 'sg-1234567'},
        'SourceSecurityGroupId': {'type': CFNString,
                                  'description': 'SourceSecurityGroupId',
                                  'default': ''}
    }

    def add_conditions(self):
        """ Create Conditions """
        template = self.template
        variables = self.get_variables()

        template.add_condition(
            'UseCidrIp',
            Not(Equals(variables['CidrIp'].ref, '')))
        template.add_condition(
            'UseSourceSecurityGroupId',
            Not(Equals(variables['SourceSecurityGroupId'].ref, '')))

    def create_security_groups_ingress(self):
        """ Creates ingress rule for elb security groups """
        template = self.template
        variables = self.get_variables()

        cidringress = template.add_resource(
            ec2.SecurityGroupIngress(
                'SecurityGroupIngressCidr',
                FromPort=variables['FromPort'].ref,
                ToPort=variables['ToPort'].ref,
                GroupId=variables['GroupId'].ref,
                IpProtocol=variables['IpProtocol'].ref,
                CidrIp=variables['CidrIp'].ref,
                Condition='UseCidrIp'
            )
        )
        securitygroupingress = template.add_resource(
            ec2.SecurityGroupIngress(
                'SecurityGroupIngressSecurityGroupId',
                FromPort=variables['FromPort'].ref,
                ToPort=variables['ToPort'].ref,
                GroupId=variables['GroupId'].ref,
                IpProtocol=variables['IpProtocol'].ref,
                SourceSecurityGroupId=variables['SourceSecurityGroupId'].ref,
                Condition='UseSourceSecurityGroupId'
            )
        )
        template.add_output(
            Output(
                cidringress.title,
                Description='Security group ingres rule for client',
                Export=Export(Sub('${AWS::StackName}-%s' % cidringress.title)),  # nopep8 pylint: disable=C0301
                Value=Ref(cidringress),
                Condition='UseCidrIp'
            )
        )
        template.add_output(
            Output(
                securitygroupingress.title,
                Description='Security group ingres rule for client',
                Export=Export(Sub('${AWS::StackName}-%s' % securitygroupingress.title)),  # nopep8 pylint: disable=C0301
                Value=Ref(securitygroupingress),
                Condition='UseSourceSecurityGroupId'
            )
        )

    def create_template(self):
        """ Boilerplate for CFN Template """
        self.template.add_version('2010-09-09')
        self.template.add_description('Create Ingress rules for Security Groups - 1.0.0')  # nopep8 pylint: disable=C0301
        self.add_conditions()
        self.create_security_groups_ingress()


# Helper section to enable easy blueprint -> template generation
# (just run `python <thisfile>` to output the json)
if __name__ == "__main__":
    from stacker.context import Context

    standalone_output.json(
        blueprint=SecurityGroupsIngress('test',
                                        Context({"namespace": "test"}),  # nopep8 pylint: disable=C0301
                                        None)
    )
