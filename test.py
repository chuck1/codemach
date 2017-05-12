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

    print_yb("sheets tests")

    for t in [
            "sheets.tests.set_cell",
            "sheets.tests.set_script_pre",
            ]:
        m = __import__(t, fromlist=["test"])
        
        print_yb(m)
        try_func(m.test)

if __name__ == "__main__":
    test()

