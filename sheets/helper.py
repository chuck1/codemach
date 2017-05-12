import numpy
import traceback
import termcolor
import sys
import io

def cells_strings(cells):
    def f(c):
        if c is None: return ""
        return c.string
    return numpy.array(numpy.vectorize(f, otypes=[str])(cells).tolist())

def cells_values(cells, sheet):
    def f(c):
        if c is None: return None
        return c.get_value(sheet)
    return numpy.vectorize(f)(cells)

class CellHelper(object):
    def __init__(self, r, c):
        self.r = r
        self.c = c

class CellsHelper(object):
    """
    we must be careful not to expose too much to the user
    such that he or she may break the program or cause security issues

    WARNING
    passing the sheet to this object is not OK for final implementation
    """
    def __init__(self, sheet):
        self.sheet = sheet

    def __getitem__(self, args):
        #if not isinstance(args, tuple): args = (args,)

        #r, c = CellsHelper.expand_args(*args)
        
        #return cells_values(self.cells.cells[r,c])
        return cells_values(self.sheet.cells.cells[args], self.sheet) 

    @classmethod
    def expand_args(cls, r, c=None):
        return r, c


