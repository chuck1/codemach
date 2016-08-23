#!/usr/bin/env python

import sys
import os
import Cookie

#sys.path.append("/home/chuck/git/python_spreadsheet")

import python_spreadsheet as ss
import python_spreadsheet.mycgi

c = Cookie.SimpleCookie(os.environ["HTTP_COOKIE"])

ss.mycgi.gen(c)




