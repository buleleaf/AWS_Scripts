#!/usr/bin/env python3
"""Take an aws credentials file and export the default section as bash vars"""
import argparse
import configparser
import os
 
 
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("credentials")
    parser.add_argument("-s", "--section", action='store', default='default')
    args = parser.parse_args()
    config = configparser.ConfigParser()
    if not os.path.exists(args.credentials):
        print('File missing.')
        quit()
    config.read(args.credentials)
    for key, value in config[args.section].items():
        print('export {}="{}"'.format(key.upper(), value))
 
 
if __name__ == '__main__':
    main()