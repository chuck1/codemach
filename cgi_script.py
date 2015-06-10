#!/usr/bin/env python

import sys
import os
import Cookie

sys.path.append("/home/chuck/git/python_spreadsheet")

import spreadsheet as ss
import spreadsheet.mycgi

c = Cookie.SimpleCookie(os.environ.get("HTTP_COOKIE"))

ss.mycgi.gen(c)




