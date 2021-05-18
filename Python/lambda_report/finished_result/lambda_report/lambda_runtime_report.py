import boto3
import functools

@functools.lru_cache()
def describe_regions():
    client = boto3.client('ec2')
    response = client.describe_regions()
    return [r['RegionName'] for r in response['Regions']]


class AWSLambda:
    def __init__(self, region):
        self._client = boto3.client('lambda', region)
        self._region = region
        self._accountalias = boto3.client('iam').list_account_aliases()

    def get_account_alias(self):
        yield self._accountalias['AccountAliases'][0]


    def list_functions(self, **kwargs):
        for page in self._client.get_paginator(
            'list_functions'
        ).paginate(**kwargs):
            for function in page['Functions']:
                function['region'] = self._region
                yield function



def get_function_name(function):
    return function['FunctionName']


# def get_function_runtime(function):
#     return function['Runtime']


def python27_runtime_filter(function):
    return function['Runtime'] == 'python2.7'



def main():

    regions = describe_regions()
    report = []

    for region in regions:
        lambda_filter = filter(python27_runtime_filter, AWSLambda(region).list_functions())


    for lf in lambda_filter:
        report.append(lf['FunctionName'][0])
    
    print(report)
        # for function in filter(python27_runtime_filter, AWSLambda(region).list_functions()):
        #     for functions in function:
        #         report.append(functions({'FunctionName'}))

    # for region in regions:
    #     for function in filter(python27_runtime_filter, AWSLambda(region).list_functions()):
    #         report.append(({FunctionName, Region, AccountAlias}))




            # print(function)
    # print(report)



# def write_lambda_function_csv(filename='{}-lambda_funtions_python2.csv'.format()):
#     """Writes output of Lambda Functions to CSV file"""
#     with open(filename, newline='') as csvfile:
#         return [w for w in csv.write(csvfile)]

# def add_csv_to_set(ec2_instances):
#     for instances in read_instance_names_from_file():
#         for i in instances:
#             ec2_instances.add(i)
#     return instances

# region = 'us-west-2'

# client = boto3.client('lambda', region)


#     print(get_function_name())
    # functions = list_functions()

    # for function in functions:
    #     pprint.pprint(function)

    # function = []


    # print(get_function_runtime())

    # for r in runtime:
    #     print(r)

if __name__ == '__main__':
    main()