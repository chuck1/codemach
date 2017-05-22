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

import sheets.cells
import sheets.script
#import sheets.helper
import sheets.exception

logger = logging.getLogger(__name__)

APPROVED_MODULES = [
        "math",
        "numpy",
        "time",
        ]

APPROVED_DEFAULT_BUILTINS = {
        '__build_class__': __build_class__,
        '__name__': 'module',
        "Exception": Exception,
        'dir': dir,
        'globals': globals,
        'list': list,
        'object': object,
        'print': print,
        'range': range,
        "repr": repr,
        'sum': sum,
        "type": type,
        }

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

def protector(f):
    def wrapper(*args):
        print('inside protector wrapper call')
        stack = inspect.stack()
        print('stack:')
        for s in stack:
            print('  ',s.filename)
            if s.filename[:5] == "<cell":
                raise sheets.exception.NotAllowedError('stopped by protector')
        return f(*args)
    return wrapper

class Book(object):
    """
    Book class
    """
    def __init__(self):
        
        self.script_pre = sheets.script.Script()
        """
        ``Script`` object that runs before cell evalutation.
        It has access to cell strings.
        The globals dict passed to this script is then used in cell evaluation.
        So cells have access to globals created or modified
        by this script.
        """

        self.script_post = sheets.script.Script()
        """
        ``Script`` object that runs after cell evaluation.
        It has access to cell strings and values.
        """

        self.sheets = {"0": Sheet(self)}

    def __getstate__(self):
        return dict((k, getattr(self, k)) for k in ['sheets', 'script_pre', 'script_post'])

    @protector
    def test_func(self):
        print('this is a test function of Book')

    def builtin___import__(self, name, globals=None, locals=None, 
            fromlist=(), level=0):
        
        name_split = name.split('.')
        
        if not name_split[0] in APPROVED_MODULES:
            raise ImportError("module '{}' is not allowed".format(name_split[0]))

        return __import__(name, globals, locals, fromlist, level)

    def builtin_open(self, file, mode='r'):
        logger.warning("invoking Book.builtin_open({}, {})".format(file, mode))

        #file = open(file, mode)

        test_fs = fs.osfs.OSFS(os.path.join(os.environ['HOME'], 'web_sheets','filesystems','test'))
        file = test_fs.open(file, mode)

        return WrapperFile(file)

    def builtin_getattr(self, *args):
        logger.warning("invoking Book.builtin_getattr({})".format(args))
        obj = args[0]
        logger.warning("obj={}".format(obj))
        
        # temporarily removed for teting of special helper module importing
        """
        import sheets.helper
        if isinstance(obj, sheets.helper.CellsHelper):
            raise sheets.exception.NotAllowedError(
                    "For security, getattr not allowed for CellsHelper objects")
        """

        return getattr(*args)

    def reset_globals(self):
        approved_builtins = {
                '__import__': self.builtin___import__,
                'getattr': self.builtin_getattr,
                'open': self.builtin_open,
                }

        approved_builtins.update(APPROVED_DEFAULT_BUILTINS)

        self.glo = {
                "__builtins__": approved_builtins,
                "sheets": dict((k, s.cells_strings()) for k, s in self.sheets.items()),
                'book': self,
                '_global__book': self,
                }

        #module = __import__('sheets.helper', globals=g, fromlist=['*'])
        
        #print()
        #print(module)
        #print(module.__file__)
        #print(dir(module))
        #print()
        

    def set_script_pre(self, s):
        if self.script_pre.set_string(s):
            self.do_all()

    def set_script_post(self, s):
        if self.script_post.set_string(s):
            self.do_all()

    def do_all(self):
        self.reset_globals()

        self.script_pre.execute(self.glo)
        
        self.cell_stack = list()
        for s in self.sheets.values():
            s.reset_globals()
            s.cells.evaluate(self, s)

        self.script_post.execute(self.glo)

    def set_cell(self, k, r, c, s):
        if not k in self.sheets:
            self.sheets[k] = Sheet(self)
        sheet = self.sheets[k]
        
        sheet.cells.set_cell(r, c, s)
        
        self.do_all()

class Sheet(object):
    def __init__(self, book):
        self.__book = book
        self.cells = sheets.cells.Cells()
        
    def __getstate__(self):
        return dict((k, getattr(self, k)) for k in ['cells'])
    
    def set_cell(self, r, c, s):
        self.cells.set_cell(r, c, s)

        self.__book.do_all()

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
        
        self.glo = dict(self.__book.glo)

        self.glo.update({
            'sheet': self,
            '_global__sheet': self,
            })

        filename = os.path.join(os.path.dirname(sheets.__file__), 'helper.py')
        
        with open(filename) as f:
            exec(f.read(), self.glo)
        
        """
        self.glo.update({
            "CellHelper": self.glo['CellHelper'],
            "SheetHelper": self.glo['SheetHelper'],
            "BookHelper": self.glo['BookHelper'],
            })
        """

    def array_values(self, *args):
        print('Sheet array_values', args)
        print('Sheet array_values', *args)

        #def cells_values(cells, book, sheet):
        def f(c):
            if c is None: return None
            v = c.get_value(self.__book, self)
            #print("cells_values cell ({},{}) s = {} v = {}".format(
            #    c.r, c.c, repr(c.string), repr(v)))
            return v
    
        #a = numpy.vectorize(f, otypes=[object])(self.cells.cells.__getitem__(*args))
        a = numpy.vectorize(f, otypes=[object])(self.cells.cells.__getitem__(args))
        #a = numpy.vectorize(f, otypes=[object])(self.cells.cells[*args])
        #a = numpy.vectorize(f, otypes=[object])(self.cells.cells[args])
        #a = numpy.vectorize(f, otypes=[object])(self.cells.cells[r, c])
        return a

    def __getitem__(self, args):
        print('Sheet __getitem__', args)
        print('Sheet __getitem__', *args)
        return self.array_values(*args)



