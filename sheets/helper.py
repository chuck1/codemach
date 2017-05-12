import numpy
import traceback
import termcolor
import sys
import io

class CellHelper(object):
    def __init__(self, r, c):
        self.r = r
        self.c = c

def cells_values(cells):
    def f(c):
        if c is None: return None
        return c.value
    return numpy.vectorize(f)(cells)

class CellsHelper(object):
    """
    we must be careful not to expose too much to the user
    such that he or she may break the program or cause security issues

    WARNING
    passing the sheet to this object is not OK for final implementation
    """
    def __init__(self, cells):
        self.cells = cells

    def __getitem__(self, args):
        #if not isinstance(args, tuple): args = (args,)

        #r, c = CellsHelper.expand_args(*args)
        
        #return cells_values(self.cells.cells[r,c])
        return cells_values(self.cells.cells[args]) 

    @classmethod
    def expand_args(cls, r, c=None):
        return r, c


