""" Load dependencies """
import awacs.sts
from awacs.aws import Allow, Policy, Principal, Statement


def assumerolepolicy(service):
    """ Boilerplate AWS service assume role policy document """
    return Policy(
        Version='2012-10-17',
        Statement=[
            Statement(
                Effect=Allow,
                Action=[awacs.sts.AssumeRole],
                Principal=Principal('Service',
                                    ['%s.amazonaws.com' % service])
            )
        ]
    )
