#!/usr/bin/env python3

import termcolor
import traceback

def print_yb(s):
    print(termcolor.colored(s,'yellow',attrs=['bold']))

def try_func(f):
    try:
        f()
    except Exception as e:
        print(termcolor.colored('failed','red',attrs=['bold']))
        print(e)
        traceback.print_exc()
        return

def tests():

    import sheets.test.set_cell
    import sheets.test.set_exec

    print_yb('sheets tests')
    print_yb('  set_cell')
    try_func(sheets.test.set_cell.test)
    print_yb('  set_exec')
    try_func(sheets.test.set_exec.test)

tests()

