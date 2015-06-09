#!/usr/bin/env python

import sys

sys.path.append("/home/chuck/git/python/projects")

import spreadsheet as ss

if __name__ == '__main__':
    req = ss.Request('stop')
    try:
        req.do()
    except:
        pass


