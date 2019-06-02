#!/usr/bin/env python3
"""Generate the CSV for the ELS Monthly Report from CSV files."""
import os
import csv
import argparse
 
 
NEW_KEYS = ('Application', 'Environment')
WANTED_FIELDS = ('Name', 'Created Time', 'Ticket Id', 'Initiated By', 'Outage Time', 'Application', 'Environment')
NAME_STRIPS = ('-Status-Check-Failed', '-Status-Check-Faile')
 
 
def clean_name(name):
    """Clean name of any extra alarm title items."""
    for key in NAME_STRIPS:
        name = name.strip(key)
    return name
 
 
def munge_row(row):
    """Return the row with old our desired fields."""
    new_row = {}
    for key in WANTED_FIELDS:
        new_row[key] = row.get(key, '')
    new_row['Initiated By'] = 'User'
    if row['Requester Email'] in ('no-reply@sns.amazonaws.com',):
        new_row['Initiated By'] = 'System'
    new_row['Outage Time'] = row['Resolution Time (in Hrs)']
    return new_row
 
 
def myfilter(row):
    """Filter out anything that doesn't match desired qualifications."""
    if 'OK' in row.get('Subject'):
        return False
    if '"' not in row.get('Subject'):
        return False
    if ('Status-Check-Failed' in row.get('Subject') or
            'StatusCheckFailed' in row.get('Subject') or
            'Status-Check-Failed' in row.get('Description') or
            'StatusCheckFailed' in row.get('Description')):
        return True
    return False
 
 
def enhance_row(row, tags):
    """Add extra tags from our tags to the row."""
    name = clean_name(row['Subject'].split('"')[1])
    row['Name'] = name
    tag_set = tags.get(name)
    if tag_set:
        # print(f'Found tags for {name}')
        for k in NEW_KEYS:
            # print('{}: {}: {}'.format(name, k, tag_set.get(k)))
            row[k] = tag_set.get(k)
    else:
        print(f'Unable to find tags for {name}')
    return row
 
 
def main():
    """Main."""
    parser = argparse.ArgumentParser()
    parser.add_argument('infile')
    parser.add_argument('outfile')
    parser.add_argument('--tags_file', '-t', action='append')
    args = parser.parse_args()
    if not os.path.exists(args.infile):
        print('Missing infile.')
        quit(1)
    tags = {}
    for fname in args.tags_file:
        with open(fname) as tags_file:
            reader = csv.DictReader(tags_file)
            tags.update(**{i.get('Name'): i for i in reader})
    with open(args.infile) as infile:
        reader = csv.DictReader(infile)
        with open(args.outfile, 'w') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=WANTED_FIELDS)
            writer.writeheader()
            [writer.writerow(munge_row(enhance_row(row, tags))) for row in reader if myfilter(row)]
 
if __name__ == '__main__':
    main()