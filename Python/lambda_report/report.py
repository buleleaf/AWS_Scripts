from aws import ListFunctions
import csv



def get_function_name(function):
    return function['FunctionName']
    # # return [x for x in list_functions(['FunctionName'])]
    # for function in list_functions():
    #     return function['FunctionName']


def get_function_runtime(function):
    return function['Runtime']
    # for function in list_functions():
    #     return function['Runtime']

# def generate_csv(filename, region):
#     filename = '{}-lambda_report.csv'.format(region)
#     with open(filename, newline='') as csvfile:
#         writer = csv.writer(csvfile )
#         return [r for r in csv.writer(csvfile)]

# def add_lambda_to_csv():
#     for lambda_name in get_function_name():
#         for i in instances:
#             ec2_instances.add(i)
#     return instances
    