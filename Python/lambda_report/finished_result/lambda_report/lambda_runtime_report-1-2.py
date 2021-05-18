import csv
import functools

import boto3

CSV_HEADERS = ('FunctionName', 'Region', 'AccountAlias')

def parse_args():
    return {'output': 'python2.7-lambdas.csv', 'onica_only': True}

@functools.lru_cache()
def describe_regions():
    client = boto3.client('ec2', 'us-east-1')
    response = client.describe_regions()
    return [r['RegionName'] for r in response['Regions']]


class AWSLambda:
    def __init__(self, region):
        self._client = boto3.client('lambda', region)
        self._region = region
        self._accountalias = boto3.client('iam').list_account_aliases()[
            'AccountAliases'
        ][0]

    def list_functions(self, **kwargs):
        for page in self._client.get_paginator('list_functions').paginate(
            **kwargs
        ):
            for function in page['Functions']:
                function['region'] = self._region
                function['account'] = self._accountalias
                yield function


def python27_runtime_filter(function):
    return function['Runtime'] == 'python2.7'


def is_onica_lambda(function):
    if 'els' in function['FunctionName'].lower() and not function.get('Tags'):
        return True
    else:
        # import code;code.interact(local={**globals(), **locals()})
        pass
    return False


def format_report(function):
    return {
        'FunctionName': function['FunctionName'],
        'Region': function['region'],
        'AccountAlias': function['account'],
    }




def write_report_to_csv(filename, rows):
    with open(filename, 'w') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=CSV_HEADERS)
        writer.writeheader()
        return writer.writerows(rows)


def run_filters(filters, data):
    for _filter in filters:
        data = filter(_filter, data)
    return data


def format_data(data, formatter=format_report):
    return map(formatter, data)


def region_lambda_report(region, filters):
    return format_data(run_filters(filters, AWSLambda(region).list_functions()))


def regions_lambda_reporter(filters, regions=describe_regions()):
    for region in regions:
        for function in region_lambda_report(region, filters):
            yield function


def build_filter_lists(args):
    filters = [python27_runtime_filter]

    if args['onica_only']:
        filters.append(is_onica_lambda)
    return filters


def main(args=parse_args()):
    write_report_to_csv(
        args['output'], regions_lambda_reporter(build_filter_lists(args))
    )


if __name__ == '__main__':
    main()
