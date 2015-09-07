#!/usr/bin/env python

import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-b', action='store_true')

args = parser.parse_args()

if args.b:
    f = open('/tmp/python_spreadsheet.log','w')
    sys.stdout = f
    sys.stderr = f

sys.path.append("/home/chuck/git/python_spreadsheet")

import python_spreadsheet as ss
import python_spreadsheet.service

s = ss.service.Service()

s.run()

