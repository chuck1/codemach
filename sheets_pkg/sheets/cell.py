import numpy
import traceback
import sys
import io

#import sheets.helper
import sheets.exception

class RecursiveCellRef(Exception): pass

class Cell(object):
    """
    Cell data is stored in the ``string`` member which can be None 
    or a string representing a python expression.
    A Cell can return a value which can be one of the following:
    
    - None if _string_ is None
    - an ``Exception`` raised by the ``compile`` function
    - an ``Exception`` raised by the ``eval`` function
    - result of the ``eval`` function
    """
    
    def __init__(self, r, c, string=None):
        """
        :param int r: row index
        :param int c: column index
        """
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
        self.comp(sheet)
        
    def comp(self, sheet):
        """
        Compile the string.
   
        The code object is inspected for possible security issues by the
        :py:func:`sheets.cell.Cell.check_code` function.
        """
        self.comp_exc = None

        if not self.string:
            self.code = None
            return
        
        try:
            self.code = compile(self.string, "<cell {},{}>".format(self.r,self.c), 'eval')
        except Exception as e:
            self.code = None
            self.comp_exc = e

        try:
            sheet.book.middleware_security.call_check_cell_code(self)
        except sheets.exception.NotAllowedError as e:
            self.code = None
            self.comp_exc = e
    

    def get_globals(self, book, sheet):
        
        g = dict(sheet.get_globals())
 
        return g

    def evaluate(self, book, sheet):
        
        if not hasattr(self, "comp_exc"): self.comp(sheet)

        if self.comp_exc is not None:
            self.value = 'compile error: '+str(self.comp_exc)
            return

        if self.code is None:
            self.value = None
            return

        g = self.get_globals(book, sheet)

        try:
            res = book.middleware_security.call_cell_eval(book, self, self.code, g)
            self.value = res.return_value
        except RecursiveCellRef as e:
            raise
        except Exception as e:
            #print("exception during cell({},{}) eval".format(self.r, self.c))
            #print(repr(e))
            traceback.print_exc()
            
            self.exception_eval = e

            #self.value = "eval error: " + str(e)
            self.value = e
        else:
            self.exception_eval = None

    def get_value(self, book, sheet):

        #print("Cell.get_value ({},{}) s = {} v = {} evaluated = {}".format(
        #    self.r, self.c, repr(self.string), 
        #    repr(self.value) if hasattr(self, 'value') else 'no value', self.evaluated))

        if self.evaluated: return self.value

        if self in book.cell_stack:
            #raise RecursiveCellRef()
            raise RuntimeError("recursion")

        book.cell_stack.append(self)

        self.evaluate(book, sheet)
        self.evaluated = True

        book.cell_stack.pop()

        return self.value



