import os
import csv
from itertools import chain

with open('status-check-alarms.csv', 'r') as f:
    reader = csv.reader(f)
    cw_alarms = list(reader)

for alarms in cw_alarms:
	for alarm in alarms:
		# print(alarm)
		os.system(f"aws cloudwatch delete-alarms --alarm-names {alarm}")
		print(f"Removing CW Alarm: {alarm}")