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

def cells_values(cells, book, sheet):
    def f(c):
        if c is None: return None
        v = c.get_value(book, sheet)
        #print("cells_values cell ({},{}) s = {} v = {}".format(c.r, c.c, repr(c.string), repr(v)))
        return v
    a = numpy.vectorize(f, otypes=[object])(cells)
    return a

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
    def __init__(self, book, sheet):
        self.book = book
        self.sheet = sheet

    def __getitem__(self, args):
        #if not isinstance(args, tuple): args = (args,)

        r, c, k = CellsHelper.expand_args(*args)
        
        if k is None:
            s = self.sheet
        else:
            s = self.book.sheets[k]
        
        return cells_values(s.cells.cells[r, c], self.book, s) 

    @classmethod
    def expand_args(cls, r, c=None, k=None):
        return r, c, k


