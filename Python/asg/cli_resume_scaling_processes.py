import os
import csv
from itertools import chain

with open('test.csv', 'r') as f:
    reader = csv.reader(f)
    autoscaling_groups = list(reader)

with open('resume_processes.csv', 'r') as f:
    reader = csv.reader(f)
    resume_processes = list(reader)

for asg in autoscaling_groups:
	for sp in asg:
		for resume_process in resume_processes:
			os.system(f"aws autoscaling resume-processes --auto-scaling-group-name {sp} --scaling-processes {resume_process}")
		# print(sp)
