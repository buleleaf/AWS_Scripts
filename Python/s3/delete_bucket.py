import os
import csv
from itertools import chain

with open('buckets.csv', 'r') as f:
    reader = csv.reader(f)
    buckets = list(reader)

for bucket in buckets:
    for s3 in bucket:
        os.system(f'aws s3 rb {s3} --force')
