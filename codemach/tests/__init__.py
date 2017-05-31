import unittest
import types
import dis
from codemach import Machine

def code_info(c):
    print('------------')
    print(dir(c))
    print('argcount ',c.co_argcount)
    print('consts   ',c.co_consts)
    print('names    ',c.co_names)
    print('varnames ',c.co_varnames)
    dis.dis(c)
    print('------------')
    for const in c.co_consts:
        if isinstance(const, types.CodeType):
            code_info(const)


def test(e, s, mode):
    c = compile(s, '<string>', mode)

    code_info(c)

    print(e.exec(c))
    print()

class Tests(unittest.TestCase):

    def test(self):
        e = Machine()
        e.verbose = 1
    
        s = """def func(a, b):\n  c = 4\n  return a + b + c\nfunc(2, 3)"""
        test(e, s, 'exec')
        
        s = """object.__getattribute__(object, '__class__')"""
        test(e, s, 'eval')
        
        s = """import math"""
        test(e, s, 'exec')
    
        s = """2 == 3"""
        test(e, s, 'eval')
    
        s = """c = 4\ndef func():\n  a = 2\n  b = 3\n  return a + b + c\nfunc()"""
        test(e, s, 'exec')
    
        s = """import math\ndef func():\n  return math.pi\nfunc()"""
        test(e, s, 'exec')
    
        s = """import datetime\ndatetime.datetime.now()"""
        test(e, s, 'exec')
    
        s = """x=1\ny=1\nx-y\nx/y\nx//y\nx%y\nx**y\n-x\n+x"""
        test(e, s, 'exec')
    
    
