#!/usr/bin/env python

import sys

sys.path.append("/home/chuck/git/python_spreadsheet")

import spreadsheet as ss
import spreadsheet.service

s = ss.service.Service()

s.run()

