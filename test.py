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
        raise

def test():

    import sheets.tests.set_cell
    import sheets.tests.set_exec

    print_yb('sheets tests')
    print_yb('  set_cell')
    try_func(sheets.tests.set_cell.test)
    print_yb('  set_exec')
    try_func(sheets.tests.set_exec.test)

if __name__ == "__main__":
    test()

