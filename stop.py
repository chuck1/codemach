#!/usr/bin/env python

import sys

sys.path.append("/home/chuck/git/python/projects")

import python_spreadsheet as ss
import python_spreadsheet.service

if __name__ == '__main__':
    req = ss.service.Request('stop')
    try:
        req.do()
    except:
        pass


