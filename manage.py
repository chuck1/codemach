#!/usr/bin/env python

import os
import argparse



def flush(args):
    print "flush"
    os.remove(os.path.join("python_spreadsheet","data","sheets.bin"))

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers()

parser_flush = subparsers.add_parser('flush')
parser_flush.set_defaults(func=flush)

args = parser.parse_args()
args.func(args)



