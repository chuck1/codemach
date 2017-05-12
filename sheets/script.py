import numpy
import traceback
import termcolor
import sys
import io


class Script(object):
    def __init__(self):
        self.string = ""
    
    def __getstate__(self):
        return dict((k, getattr(self, k)) for k in ["string"])
    
    def set_string(self,s):
        if s == self.string: return
        self.string = s
        self.comp()

    def comp(self):
        try:
            self.code = compile(self.script, '<script>', 'exec')
        except Exception as e:
            self.code = None
            self.comp_exc = e

            l = traceback.format_exc().split("\n")
            #l.pop(1)
            #l.pop(1)
            self.output = "\n".join(l)
            return
        else:
            self.comp_exc = None

    def execute(self, g):
        if not hasattr(self, "code"): self.comp()

        if self.code is None: return

        out = io.StringIO()

        old = sys.stdout
        sys.stdout = out
        try:
            exec(self.code_exec, g)
        except Exception as e:
            sys.stdout = old

            self.exec_exception_exec = e

            exc_string = traceback.format_exc().split('\n')
            #exc_string.pop(1)
            #exc_string.pop(1)
            exc_string = "\n".join(exc_string)
        else:
            sys.stdout = old
            self.exec_exception_exec = None
            exc_string = ''
       
        self.output = out.getvalue() + "".join(exc_string)

        # inspect the cells global
        try:
            cells = self.glo["cells"]

            print()
            print("after script exec")
            print("cells")
            print(repr(cells))

            if not isinstance(cells, numpy.ndarray):
                raise TypeError("cells is not a numpy array")

            print("ndim:", repr(cells.ndim))

            if cells.ndim != 2:
                raise TypeError("cells does not have dimension of 2")

            print("dtype:", repr(cells.dtype))

            if cells.dtype != numpy.dtype("<U1"):
                raise TypeError("cells dtype is not '<U1'")

        except Exception as e:
            print(e)





