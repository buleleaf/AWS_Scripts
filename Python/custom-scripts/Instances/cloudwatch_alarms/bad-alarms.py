import boto3
import os

REGION = os.getenv('AWS_REGION', 'us-west-2')
client = boto3.client('cloudwatch', REGION)

def divide_chunks(l, n): 
      
    # looping till length l 
    for i in range(0, len(l), n):  
        yield l[i:i + n] 


with open('bad-alarms.csv') as infile:
    alarms = [a.strip() for a in infile.readlines()]
    for chunk in divide_chunks(alarms, 100):
        response = client.delete_alarms(AlarmNames=chunk)
        print(response)

