""" Load dependencies """
from troposphere import cloudformation


class AMILookup(cloudformation.AWSCustomObject):
    """ Class for AMI lookup custom resource """
    resource_type = "Custom::AMILookup"

    props = {
        'ServiceToken': (basestring, True),
        'Platform': (basestring, True),
        'Region': (basestring, True)
    }


class SubnetLookup(cloudformation.AWSCustomObject):
    """ Class for subnet lookup custom resource """
    resource_type = "Custom::SubnetLookup"

    props = {
        'ServiceToken': (basestring, True),
        'CoreVPCStack': (basestring, True),
        'Region': (basestring, True)
    }
