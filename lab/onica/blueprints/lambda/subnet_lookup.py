"""Finds the subnets created by the core stack - v1.0.0"""

import boto3
import cfnresponse  # pylint: disable=E0401


def handler(event, context):
    """ Lambda entry point """

    region = event['ResourceProperties']['Region']
    stack_name = event['ResourceProperties']['CoreVPCStack']

    client = boto3.client('cloudformation', region_name=region)
    describe_response = client.describe_stacks(StackName=stack_name)

    response_data = {}
    public_subnets = {}
    private_route_tables = {}
    if 'Stacks' in describe_response and len(describe_response['Stacks']) == 1:
        response_code = cfnresponse.SUCCESS
        # Loop through outputs and find needed values
        for out in describe_response['Stacks'][0]['Outputs']:
            if out['OutputKey'] == 'PublicRouteTable':
                response_data['PublicRouteTableId'] = out['OutputValue']
            elif out['OutputKey'].startswith('PrivateRouteTable'):
                private_route_tables[out['OutputKey']] = out['OutputValue']
            elif out['OutputKey'].startswith('PubSubnet'):
                public_subnets[out['OutputKey']] = out['OutputValue']

        # Sort the found values and add to response hash
        private_route_table_l = []
        for key in sorted(private_route_tables.iterkeys()):
            private_route_table_l.append(private_route_tables[key])
        response_data['PrivateRouteTables'] = ' '.join(private_route_table_l)

        public_subnet_l = []
        for key in sorted(public_subnets.iterkeys()):
            public_subnet_l.append(public_subnets[key])
        response_data['PublicSubnetList'] = public_subnet_l
    else:
        response_code = cfnresponse.FAILED
        response_data['Data'] = describe_response['ResponseMetadata']

    cfnresponse.send(event,
                     context,
                     response_code,
                     response_data,
                     False)  # physicalResourceId
