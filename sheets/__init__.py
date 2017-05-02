

import numpy
import traceback


class Cell(object):
    def __init__(self,r,c):
        self.string = None
        self.r = r
        self.c = c

    def set_string(self,sheet,s):
        if s == self.string: return
        self.string = s
        self.comp()
        self.calc(sheet)
        
    def comp(self):
        self.code = compile(
                self.string,
                "<cell {},{}>".format(self.r,self.c),
                'eval')

    def calc(self,sheet):
        self.value = eval(self.code,sheet.get_globals())

class Sheet(object):
    def __init__(self):
        self.cells = numpy.empty((0,0),dtype=object)
        self.globals = {'__builtins__':{'__import__':self.builtin___import__}}
        self.string_exec = None
    
    def builtin___import__(self, name, globals=None, locals=None, fromlist=(), level=0):
        approved_modules = [
                'math']
        name_split = name.split('.')
        """
        print('name    ',name)
        print('globals ',globals)
        print('locals  ',locals)
        print('fromlist',fromlist)
        print('level   ',level)
        """
        if not name_split[0] in approved_modules:
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
    
    def get_globals(self):
        return self.globals

    def set_exec(self,s):
        if s == self.string_exec: return

        self.string_exec = s

        try:
            self.code_exec = compile(
                    self.string_exec,
                    '<string exec>',
                    'exec')
        except Exception as e:
            self.compile_exception_exec = traceback.format_exc()
            raise e
        else:
            self.compile_exception_exec = None


        try:
            exec(self.code_exec,self.get_globals())
        except Exception as e:
            self.exec_exception_exec = traceback.format_exc()
            raise e
        else:
            self.exec_exception_exec = None
        




