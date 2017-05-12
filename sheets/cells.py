import numpy
import traceback
import termcolor
import sys
import io

import sheets.cells

class Cells(object):
    def __init__(self):
        self.cells = numpy.empty((0,0),dtype=object)
        self.ensure_size(0,0)
    
    def __getstate__(self):
        return dict((k, getattr(self, k)) for k in ['cells'])
    
    def ensure_size(self, r, c):
        if r > (numpy.shape(self.cells)[0]-1):
            shape = (r-numpy.shape(self.cells)[0]+1,numpy.shape(self.cells)[1])
            self.cells = numpy.append(
                    self.cells,
                    numpy.empty(shape,dtype=object),
                    axis=0)

        if c > (numpy.shape(self.cells)[1]-1):
            shape = (numpy.shape(self.cells)[0],c-numpy.shape(self.cells)[1]+1)
            self.cells = numpy.append(
                    self.cells,
                    numpy.empty(shape,dtype=object),
                    axis=1)

    def set_cell(self, r, c, s):
        self.ensure_size(r, c)

        if self.cells[r,c] is None:
            self.cells[r,c] = Cell(r,c)

        self.cells[r,c].set_string(self, s)

    def add_column(self, i):
        if i is None:
            i = numpy.shape(self.cells)[1]

        self.cells = numpy.insert(self.cells, i, None, axis=1)

    def add_row(self, i):
        if i is None:
            i = numpy.shape(self.cells)[0]

        self.cells = numpy.insert(self.cells, i, None, axis=0)

    def evaluate(self):
        
        self.set_evaluated(False)

        def f(cell, r, c):
            if cell is None: return
            cell.calc(self)
        
        r = numpy.arange(numpy.shape(self.cells)[0])
        c = numpy.arange(numpy.shape(self.cells)[1])
        
        for i in range(numpy.shape(self.cells)[0]):
            for j in range(numpy.shape(self.cells)[1]):
                f(self.cells[i,j], r[i], c[j])

    def set_evaluated(self, b):
        def f(c):
            if c is not None:
                c.evaluated = b
        numpy.vectorize(f)(self.cells)

    def cells_strings(self):
        def f(c):
            if c is None: return ""
            return c.string
        return numpy.array(numpy.vectorize(f, otypes=[str])(self.cells).tolist())



