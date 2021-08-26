import argparse

parser = argparse.ArgumentParser(description='sets the environment')
parser.add_argument('environment', metavar='environment', type=str, help='enter the environment')
# parser.add_argument('-e', '--environment',action='store', type=str, help='Specify which environment')

args = parser.parse_args()

environment = args.environment


print(str(environment))