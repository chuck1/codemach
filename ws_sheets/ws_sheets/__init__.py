"""
Security
========

We must prevent script and cell code from accessing objects other
than those in :py:mod:`sheet.helper`.
This task is made difficult by the fact that Python has mechanism for
true provate variables.

Consider the following::

    getattr(cellshelper, '__globals__')

"""

import numpy
import traceback
import os
import sys
import io
import logging
import fs.osfs
import inspect
import contextlib

import sheets.cells
import sheets.script
#import sheets.helper
import sheets.exception
import sheets.context
import sheets.middleware

logger = logging.getLogger(__name__)

class WrapperFile(object):
    def __init__(self, file):
        self.file = file

    def write(self, s):
        logger.warning("involving WrapperFile.write({}, {})".format(self, s))
        logger.warning("length of s: {}".format(len(s)))
        return self.file.write(s)

    def read(self):
        logger.warning("involving WrapperFile.read({})".format(self))
        return self.file.read()

class Protector(object):
    def __init__(self, f):
        self.f = f
    def __call__(self, *args):
        print('inside Protector __call__')
        print('stack:', inspect.stack)
        print(args)
        print(*args)
        self.f(*args)


def protector1(f):
    def wrapper(book, *args):
        if object.__getattribute__(book, 'context') != sheets.context.Context.NONE:
            object.__getattribute__(book, 'middleware_security').call_book_method_decorator(
                    book, f, args)
        return f(book, *args)

    return wrapper

def context_decorator(context):
    def wrapper(f):
        def wrapped(o, *args):
            with sheets.context.context(book, context):
                return f(o, *args)
        return wrapped
    return wrapper

class Callable(object):
    def __init__(self, func):
        self.func = func

    def __call__(self, *args):
        return self.func(*args)

class Book(object):
    """
    Book class
    """
    def __init__(self, settings=None):
        self.context = sheets.context.Context.NONE
        
        self.script_pre = sheets.script.Script(self)
        """
        ``Script`` object that runs before cell evalutation.
        It has access to cell strings.
        The globals dict passed to this script is then used in cell evaluation.
        So cells have access to globals created or modified
        by this script.
        """

        self.script_post = sheets.script.Script(self)
        """
        ``Script`` object that runs after cell evaluation.
        It has access to cell strings and values.
        """

        self.sheets = {"0": Sheet(self)}

        self.cell_stack = list()
        self.glo = None

        # security testing
        self.test_callable = Callable(self.test_func_2)
    
        self.settings = settings

        # middleware
        self.middleware_security = sheets.middleware.MiddlewareSecurityManager(
                self.settings.MIDDLEWARE_SECURITY)

        """
        string to be interpreted as rst and displayed on webpage
        """
        self.docs = ''

    def get_book(self): return self

    def __getstate__(self):
        names = ['sheets', 'script_pre', 'script_post', 'settings', 'docs']
        return dict((k, getattr(self, k)) for k in names)

    def __setstate__(self, state):
        self.__dict__.update(state)
        self.context = sheets.context.Context.NONE

    #@protector1
    def __getattribute__(self, name):
        return object.__getattribute__(self, name)

    def set_docs(self, s):
        self.docs = s

    #@protector
    def test_func(self):
        print('this is a test function of Book')

    def test_func_2(self, arg1, arg2):
        return 'test_func_2 with args ' + str(arg1) +' '+ str(arg2)

    def reset_globals(self):
        res = self.middleware_security.call_book_globals(self)
        self.glo = res._globals
        
    def get_globals(self):
        if self.glo is None:
            self.reset_globals()
        return self.glo

    def set_script_pre(self, s):
        if self.script_pre.set_string(s):
            self.do_all()

    def set_script_post(self, s):
        if self.script_post.set_string(s):
            self.do_all()

    def do_all(self):
        assert(self.context == sheets.context.Context.NONE)
        self.reset_globals()

        self.script_pre.execute(self.glo)
        
        self.cell_stack = list()
        for s in self.sheets.values():
            s.reset_globals()
            s.cells.evaluate(self, s)

        assert(self.context == sheets.context.Context.NONE)
        self.script_post.execute(self.glo)

    def set_cell(self, k, r, c, s):
        if not k in self.sheets:
            self.sheets[k] = Sheet(self)
        sheet = self.sheets[k]
        
        sheet.set_cell(r, c, s)
        
        self.do_all()

    @protector1
    def __getitem__(self, key):
        if not key in self.sheets:
            self.sheets[key] = Sheet(self)
        return self.sheets[key]

class Sheet(object):
    def __init__(self, book):
        self.book = book
        self.cells = sheets.cells.Cells()
        self.glo = None

    def __getstate__(self):
        return dict((k, getattr(self, k)) for k in ['cells'])

    def get_book(self): return self.book
    
    def set_cell(self, r, c, s):
        self.cells.set_cell(self, r, c, s)

        self.book.do_all()

    def add_column(self, i):
        self.cells.add_column(i)

    def add_row(self, i):
        self.cells.add_row(i)

    def cells_evaluated_set(self, b):
        def f(c):
            if c is not None:
                c.evaluated = b
        numpy.vectorize(f)(self.cells)

    def cells_strings(self):
        return self.cells.cells_strings()

    def reset_globals(self):
        res = self.book.middleware_security.call_sheet_globals(self.book, self)
        self.glo = res._globals
        
    def get_globals(self):
        if self.glo is None:
            self.reset_globals()
        return self.glo

    def array_values(self, *args):
        def f(c):
            if c is None: return None
            v = c.get_value(self.book, self)
            return v
    
        a = numpy.vectorize(f, otypes=[object])(self.cells.cells.__getitem__(args))
        return a

    def __getitem__(self, args):
        return self.array_values(*args)

    def __setitem__(self, args, string):
        def f(cell, s, r, c):
            if cell is None:
                cell = sheets.cell.Cell(r, c)
                self.cells.cells[r, c] = cell
            cell.set_string(self, s)
        
        self.cells.ensure_size(*args)
        
        shape = numpy.shape(self.cells.cells)
        r = numpy.arange(shape[0])
        c = numpy.arange(shape[1])

        r = r[args[0]]
        c = c[args[1]]
        
        C, R = numpy.meshgrid(c, r)

        numpy.vectorize(f, otypes=[object])(self.cells.cells.__getitem__(args), string, R, C)
       
        # lazy
        self.book.do_all()





