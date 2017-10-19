import unittest
import types
import dis

from codemach.machine import Machine

def code_info(c):
    print('------------')
    print('argcount ',c.co_argcount)
    print('consts   ',c.co_consts)
    print('names    ',c.co_names)
    print('varnames ',c.co_varnames)
    dis.dis(c)
    print('------------')
    for const in c.co_consts:
        if isinstance(const, types.CodeType):
            code_info(const)

def _test(e, s, mode):
    #print('\nsource:\n{}\n'.format(s))
    c = compile(s, '<string>', mode)

    code_info(c)

    return e.exec(c)

def test_mach():
    e = Machine(verbose=True)
    
    #log_config()
    
    s = """def func(a, b):\n  return a + b\nfunc(2, 3)"""
    _test(e, s, 'exec')
    

