""" Load dependencies """

from sturdy_stacker_core_blueprints import version  # pylint: disable=W0403
from sturdy_stacker_core_blueprints.utils import standalone_output  # pylint: disable=W0403

from troposphere import (
    Equals, Export, If, Or, Ref, Join, Output, Sub, s3, GetAtt
)

import awacs.s3
from awacs.aws import Condition, Deny, Principal, Policy, Statement
# autogenerated conditions trip up pylint
from awacs.aws import Null, StringNotEquals  # pylint: disable=E0611

from stacker.blueprints.base import Blueprint
from stacker.blueprints.variables.types import CFNString


class ChefBuckets(Blueprint):
    """ Blueprint for creating S3 buckets (and optionally a KMS key) for the
        Sturdy Networks core AWS environment """

    VARIABLES = {
        'ChefBucketName': {'type': CFNString,
                           'description': 'Name of bucket storing core Chef '
                                          'configuration',
                           'default': ''},
        'ChefDataBucketName': {'type': CFNString,
                               'description': 'Name of bucket storing extra/ '
                                              'restricted Chef data',
                               'default': ''},
        'CustomerName': {'type': CFNString,
                         'description': 'The nickname for the new customer. '
                                        'Must be all lowercase letters, '
                                        'should not contain spaces or special '
                                        'characters, nor should it include '
                                        'any part of EnvironmentName.',
                         'allowed_pattern': '[-_ a-z]*',
                         'default': ''},
        'EnvironmentName': {'type': CFNString,
                            'description': 'Name of Environment',
                            'default': 'common'}
    }

    def add_conditions(self):
        """Set up template conditions."""
        template = self.template
        variables = self.get_variables()

        for i in ['ChefBucketName', 'ChefDataBucketName']:
            template.add_condition(
                "%sOmitted" % i,
                Or(Equals(variables[i].ref, ''),
                   Equals(variables[i].ref, 'undefined'))
            )

    def create_buckets(self):
        """ Creates the buckets and policies """
        template = self.template
        variables = self.get_variables()

        chefbucket = template.add_resource(
            s3.Bucket(
                'ChefBucket',
                AccessControl=s3.Private,
                BucketName=If(
                    'ChefBucketNameOmitted',
                    Ref('AWS::NoValue'),
                    variables['ChefBucketName'].ref
                ),
                LifecycleConfiguration=s3.LifecycleConfiguration(
                    Rules=[
                        s3.LifecycleRule(
                            NoncurrentVersionExpirationInDays=90,
                            Status='Enabled'
                        )
                    ]
                ),
                VersioningConfiguration=s3.VersioningConfiguration(
                    Status='Enabled'
                )
            )
        )
        template.add_output(Output(
            '%sName' % chefbucket.title,
            Description='Name of bucket storing core Chef configuration',
            Export=Export(Sub('${AWS::StackName}-%sName' % chefbucket.title)),
            Value=Ref(chefbucket)
        ))
        template.add_output(Output(
            '%sArn' % chefbucket.title,
            Description='Arn of bucket storing core Chef configuration',
            Export=Export(Sub('${AWS::StackName}-%sArn' % chefbucket.title)),
            Value=GetAtt(chefbucket, 'Arn')
        ))

        chefdatabucket = template.add_resource(
            s3.Bucket(
                'ChefDataBucket',
                AccessControl=s3.Private,
                BucketName=If(
                    'ChefDataBucketNameOmitted',
                    Ref('AWS::NoValue'),
                    variables['ChefDataBucketName'].ref
                ),
                VersioningConfiguration=s3.VersioningConfiguration(
                    Status='Enabled'
                )
            )
        )
        template.add_output(Output(
            '%sName' % chefdatabucket.title,
            Description='Name of bucket storing extra/restricted Chef data',
            Export=Export(Sub('${AWS::StackName}-'
                              '%sName' % chefdatabucket.title)),
            Value=Ref(chefdatabucket)
        ))
        template.add_output(Output(
            '%sArn' % chefdatabucket.title,
            Description='Arn of bucket storing extra/restricted Chef data',
            Export=Export(Sub('${AWS::StackName}-'
                              '%sArn' % chefdatabucket.title)),
            Value=GetAtt(chefdatabucket, 'Arn')
        ))

        # https://docs.aws.amazon.com/AmazonS3/latest/dev/UsingServerSideEncryption.html
        template.add_resource(
            s3.BucketPolicy(
                'RequireChefDataBucketEncryption',
                Bucket=Ref(chefdatabucket),
                PolicyDocument=Policy(
                    Version='2012-10-17',
                    Statement=[
                        Statement(
                            Sid='DenyIncorrectEncryptionHeader',
                            Action=[awacs.s3.PutObject],
                            Condition=Condition(
                                StringNotEquals(
                                    's3:x-amz-server-side-encryption',
                                    'AES256'
                                )
                            ),
                            Effect=Deny,
                            Principal=Principal('*'),
                            Resource=[
                                Join('', [GetAtt(chefdatabucket, 'Arn'),
                                          '/*'])
                            ]
                        ),
                        Statement(
                            Sid='DenyUnEncryptedObjectUploads',
                            Action=[awacs.s3.PutObject],
                            Condition=Condition(
                                Null(
                                    's3:x-amz-server-side-encryption',
                                    'true'
                                )
                            ),
                            Effect=Deny,
                            Principal=Principal('*'),
                            Resource=[
                                Join('', [GetAtt(chefdatabucket, 'Arn'),
                                          '/*'])
                            ]
                        )
                    ]
                )
            )
        )

    def create_template(self):
        self.template.add_version('2010-09-09')
        self.template.add_description("Prepare Chef buckets for Core "
                                      "Infrastructure - {0}".format(version()))
        self.add_conditions()
        self.create_buckets()


# Helper section to enable easy blueprint -> template generation
# (just run `python <thisfile>` to output the json)
if __name__ == "__main__":
    from stacker.context import Context

    standalone_output.json(
        blueprint=ChefBuckets('test',
                              Context({"namespace": "test"}),
                              None)
    )
