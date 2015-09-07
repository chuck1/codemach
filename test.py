#!/usr/bin/env python

import python_spreadsheet as ss

s = ss.sheet.Sheet()

s.set_cell(1,1,"hi")

func = lambda c,s: c.str_value(s)

print s.html(func)

