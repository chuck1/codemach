import numpy
import traceback
import termcolor
import sys
import io

import sheets.helper

class RecursiveCellRef(Exception): pass

class Cell(object):
    def __init__(self, r, c, string=None):
        self.r = r
        self.c = c
        self.string = string
        self.evaluated = False

    def __repr__(self):
        return "Cell({}, {}, {})".format(self.r, self.c, repr(self.string))

    def __getstate__(self):
        return dict((k, getattr(self, k)) for k in ['r', 'c', 'string'])

    def set_string(self, sheet, s):
        """
        this shall be the only method for changing the string member
        """
        if s == self.string: return
        self.string = s
        self.comp()
        
    def comp(self):

        self.comp_exc = None

        if not self.string:
            self.code = None
            return
        
        try:
            self.code = compile(self.string, "<cell {},{}>".format(self.r,self.c), 'eval')
        except Exception as e:
            self.code = None
            self.comp_exc = e

    def get_globals(self, sheet):
        g = dict(sheet.glo)

        g.update({
                'cell': sheets.helper.CellHelper(self.r, self.c),
                "cellshelper": sheets.helper.CellsHelper(sheet),
                })
        return g

    def evaluate(self, sheet):
        
        if self.comp_exc is not None:
            self.value = 'compile error: '+str(self.comp_exc)
            return

        if self.code is None:
            self.value = ""
            return

        g = self.get_globals(sheet)

        try:
            self.value = eval(self.code, g)
        except RecursiveCellRef as e:
            raise
        except Exception as e:
            print(termcolor.colored(
                "exception during cell({},{}) eval".format(self.r, self.c), "yellow", attrs=["bold"]))
            print(termcolor.colored(repr(e), "yellow", attrs=["bold"]))
            #traceback.print_exc()
            
            self.exception_eval = e

            #self.value = "eval error: " + str(e)
            self.value = e
        else:
            self.exception_eval = None

    def get_value(self, sheet):
        #print(self, self.evaluated)

        if self.evaluated: return self.value

        if self in sheet.cell_stack:
            #raise RecursiveCellRef()
            raise RuntimeError("recursion")

        sheet.cell_stack.append(self)

        self.evaluate(sheet)
        self.evaluated = True

        sheet.cell_stack.pop()

    

