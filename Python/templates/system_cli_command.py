import os
import csv
from itertools import chain

with open('buckets.csv', 'r') as f:
    reader = csv.reader(f)
    s3_buckets = list(reader)

for buckets in s3_buckets:
	for bucket in buckets:
		os.system(f"aws s3 rb {bucket} --force")