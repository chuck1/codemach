#!/usr/bin/env python

import sys

sys.path.append("/home/chuck/git/python/projects")

import spreadsheet as ss
import spreadsheet.service

s = ss.service.Service()

s.run()

