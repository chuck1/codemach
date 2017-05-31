import numpy
import traceback
import sys
import io

import sheets.cell
#import sheets.helper

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

class Cells(object):
    def __init__(self):
        self.cells = numpy.array([[sheets.cell.Cell(0, 0)]], dtype=object)
    
    def __getstate__(self):
        return dict((k, getattr(self, k)) for k in ['cells'])
    
    def ensure_size(self, r, c):
        R = numpy.shape(self.cells)[0]
        C = numpy.shape(self.cells)[1]
        
        if r > (R - 1):
            shape = (r - R + 1, C)
            self.cells = numpy.append(
                    self.cells,
                    numpy.empty(shape,dtype=object),
                    axis=0)

            for i in range(R, r + 1):
                for j in range(C):
                    #self.cells[i, j] = sheets.cell.Cell(i, j)
                    pass

        R = numpy.shape(self.cells)[0]
        C = numpy.shape(self.cells)[1]

        if c > (C - 1):
            shape = (R, c - C + 1)
            self.cells = numpy.append(
                    self.cells,
                    numpy.empty(shape,dtype=object),
                    axis=1)

            for i in range(R):
                for j in range(C, c + 1):
                    #self.cells[i, j] = sheets.cell.Cell(i, j)
                    pass

    def set_cell(self, sheet, r, c, s):
        self.ensure_size(r, c)

        if self.cells[r,c] is None:
            self.cells[r,c] = sheets.cell.Cell(r,c)

        self.cells[r,c].set_string(sheet, s)

    def add_column(self, i):
        if i is None:
            i = numpy.shape(self.cells)[1]

        self.cells = numpy.insert(self.cells, i, None, axis=1)

    def add_row(self, i):
        if i is None:
            i = numpy.shape(self.cells)[0]

        self.cells = numpy.insert(self.cells, i, None, axis=0)

    def evaluate(self, book, sheet):
        
        self.set_evaluated(False)

        def f(cell, r, c):
            if cell is None: return
            #cell.evaluate(sheet)
            cell.get_value(book, sheet)
        
        r = numpy.arange(numpy.shape(self.cells)[0])
        c = numpy.arange(numpy.shape(self.cells)[1])
        
        for i in range(numpy.shape(self.cells)[0]):
            for j in range(numpy.shape(self.cells)[1]):
                f(self.cells[i,j], i, j)

    def set_evaluated(self, b):
        def f(c):
            if c is not None:
                c.evaluated = b
        numpy.vectorize(f)(self.cells)

    def cells_strings(self):
        return cells_strings(self.cells)



