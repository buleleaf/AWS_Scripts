## Summary

1. Gets list of Lambda Functions
2. Filters by Name and Runtime
3. Filters by Runtime Version
4. Filters by Created by (Onica or Edwards (If Possible))
5. Generates report to CSV

As a stakeholder I would like to generate a list of lambda functions with a runtime of Python 2, and optionally filter that list to Onica owned lambdas, in order determine which functions need to be updated to Python 3.

0. Iterate through all regions.
1. Get list of lambda functions.
	1a. Produce generator of lambda functions.
2. Filter by runtime. 
	2a. Use a filter function.
3. Optionally, filter by created by Onica.
	3a. Potentially using tags.
4. Output report.
	4a. Function name, region, account