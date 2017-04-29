#!/usr/bin/env python

import signal, os
import sys
import argparse


parser = argparse.ArgumentParser()
#parser.add_argument('-b', action='store_true')

args = parser.parse_args()

"""
f = None

if args.b:
    f = open('/tmp/python_spreadsheet.log','w')
    sys.stdout = f
    sys.stderr = f

sys.path.append("/home/chuck/git/python_spreadsheet")
"""

import pyspreadservice

server = pyspreadservice.Server()

"""
def handler(signum, frame):
    print 'Signal handler called with signal', signum
    s.stop = True

signal.signal(signal.SIGTERM, handler)
"""

server.main_loop()

