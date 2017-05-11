import numpy
import traceback
import termcolor
import sys
import io

APPROVED_MODULES = [
        'math']

APPROVED_DEFAULT_BUILTINS = {
        '__build_class__': __build_class__,
        '__name__': 'module',
        "Exception": Exception,
        'globals': globals,
        'list': list,
        'object': object,
        'print': print,
        'range': range,
        "repr": repr,
        'sum': sum,
        "type": type,
        }

class CellHelper(object):
    def __init__(self, r, c):
        self.r = r
        self.c = c

class Cell(object):
    def __init__(self,r,c):
        self.string = None
        self.r = r
        self.c = c

    def __getstate__(self):
        return dict((k, getattr(self, k)) for k in ['r', 'c', 'string', 'value'])

    def set_string(self,sheet,s):
        if s == self.string: return
        self.string = s
        self.comp()
        self.calc(sheet)
        
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
        g = {
                'cell': CellHelper(self.r, self.c),
                }
        g.update(sheet.get_globals())
        return g

    def calc(self, sheet):
        if not hasattr(self, 'comp_exc'):
            self.comp()
        
        if self.comp_exc is not None:
            self.value = 'compile error: '+str(self.comp_exc)
            return

        if not self.code:
            self.value = ''
            return

        g = self.get_globals(sheet)

        try:
            self.value = eval(self.code, g)
        except Exception as e:
            print(termcolor.colored("exception during cell({},{}) eval".format(self.r, self.c), "yellow"))
            print(termcolor.colored(e, "yellow"))
            
            self.value = "eval error: " + str(e)

class Sheet(object):
    def __init__(self):
        self.cells = numpy.empty((0,0),dtype=object)
        
        self.ensure_size(0,0)
        
        self.script = ''
        self.script_output = ''
    
    def __getstate__(self):
        return dict((k, getattr(self, k)) for k in ['cells', 'script', 'script_output'])
    
    def builtin___import__(self, name, globals=None, locals=None, 
            fromlist=(), level=0):
        
        name_split = name.split('.')
        
        if not name_split[0] in APPROVED_MODULES:
            raise ImportError("module '{}' is not allowed".format(name_split[0]))

        return __import__(name, globals, locals, fromlist, level)

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

    def set_cell(self,r,c,s):
        self.ensure_size(r,c)

        if self.cells[r,c] is None:
            self.cells[r,c] = Cell(r,c)

        self.cells[r,c].set_string(self,s)

    def add_column(self, i):
        if i is None:
            i = numpy.shape(self.cells)[1]

        self.cells = numpy.insert(self.cells, i, None, axis=1)

    def add_row(self, i):
        if i is None:
            i = numpy.shape(self.cells)[0]

        self.cells = numpy.insert(self.cells, i, None, axis=0)

    def get_globals(self):
        if not hasattr(self, 'glo'):
            self.script_exec()
        return self.glo

    def reset_globals(self):
        approved_builtins = {
                '__import__': self.builtin___import__,}

        approved_builtins.update(APPROVED_DEFAULT_BUILTINS)

        self.glo = {
                "__builtins__": approved_builtins,
                "cells": self.cells_strings(),
                }

    def eval_all(self):
        def f(cell, r, c):
            if cell is None: return
            cell.calc(self)
        
        r = numpy.arange(numpy.shape(self.cells)[0])
        c = numpy.arange(numpy.shape(self.cells)[1])
        
        for i in range(numpy.shape(self.cells)[0]):
            for j in range(numpy.shape(self.cells)[1]):
                f(self.cells[i,j], r[i], c[j])

    def cells_strings(self):
        def f(c):
            if c is None: return None
            return c.string
        return numpy.vectorize(f, otypes=[object])(self.cells).tolist()

    def set_exec(self,s):
        if s == self.script: return
        self.script = s
        self.script_exec()

    def script_exec(self):

        self.reset_globals()

        try:
            self.code_exec = compile(self.script, '<script>', 'exec')
        except Exception as e:
            self.compile_exception_exec = e

            l = traceback.format_exc().split("\n")
            l.pop(1)
            l.pop(1)
            self.script_output = "\n".join(l)
            return
        else:
            self.compile_exception_exec = None

        out = io.StringIO()

        if 1:
            old = sys.stdout
            sys.stdout = out
            try:
                exec(self.code_exec, self.glo)
            except Exception as e:
                sys.stdout = old

                self.exec_exception_exec = e

                exc_string = traceback.format_exc().split('\n')
                exc_string.pop(1)
                exc_string.pop(1)
                exc_string = "\n".join(exc_string)
            else:
                sys.stdout = old
                self.exec_exception_exec = None
                exc_string = ''
       
        self.script_output = out.getvalue() + "".join(exc_string)

        self.eval_all()

