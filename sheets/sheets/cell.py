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

    def get_globals(self, book, sheet):
        g = dict(book.glo)
        
        g.update({
                'cell': sheets.helper.CellHelper(self.r, self.c),
                "cellshelper": sheets.helper.CellsHelper(book, sheet),
                })
        return g

    def evaluate(self, book, sheet):
        
        if not hasattr(self, "comp_exc"): self.comp()

        if self.comp_exc is not None:
            self.value = 'compile error: '+str(self.comp_exc)
            return

        if self.code is None:
            self.value = ""
            return

        g = self.get_globals(book, sheet)

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

    def get_value(self, book, sheet):
        #print(self, self.evaluated)

        #print("Cell.get_value ({},{}) s = {} v = {} evaluated = {}".format(self.r, self.c, repr(self.string), repr(self.value) if hasattr(self, 'value') else 'no value', self.evaluated))

        if self.evaluated: return self.value

        if self in book.cell_stack:
            #raise RecursiveCellRef()
            raise RuntimeError("recursion")

        book.cell_stack.append(self)

        self.evaluate(book, sheet)
        self.evaluated = True

        book.cell_stack.pop()

        return self.value

