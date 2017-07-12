import unittest
import types
import dis
import codemach
from codemach import Machine

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

def _test(_, s, mode, globals_=None):
    m = Machine(verbose=True)
    #print('\nsource:\n{}\n'.format(s))
    c = compile(s, '<string>', mode)

    code_info(c)

    return m.exec(c, globals_=globals_)

def test_mach():
    e = Machine(verbose=False)
    
    s = """def func(a, b):\n  c = 4\n  return a + b + c\nfunc(2, 3)"""
    _test(e, s, 'exec')
    
    s = """object.__getattribute__(object, '__class__')"""
    _test(e, s, 'eval')
    
    s = """import math"""
    _test(e, s, 'exec')

    s = """2 == 3"""
    _test(e, s, 'eval')

    s = """c = 4\ndef func():\n  a = 2\n  b = 3\n  return a + b + c\nfunc()"""
    _test(e, s, 'exec')

    s = """import math\ndef func():\n  return math.pi\nfunc()"""
    _test(e, s, 'exec')

    s = """import datetime\ndatetime.datetime.now()"""
    _test(e, s, 'exec')

    s = """x=1\ny=1\nx-y\nx/y\nx//y\nx%y\nx**y\n-x\n+x"""
    _test(e, s, 'exec')

    s = """class Foo(object):\n  a = 1\nfoo = Foo()"""
    _test(e, s, 'exec')
    
    s = """class Foo(object):\n  def func(self):\n    return 0\nfoo = Foo()\nfoo.func()"""
    _test(e, s, 'exec')

    s = "a=[0];b=a[0]"
    _test(e, s, 'exec')

    class Sliceable:
        def __getitem__(self, args):
            try:
                return len(args)
            except:
                return 1

    a = Sliceable()

    s = "a[0:1:2]"
    _test(e, s, 'exec', {'a':a})

    s = "a[:]"
    _test(e, s, 'exec', {'a':a})
    
    s = "a[0,0]"
    assert _test(e, s, 'eval', {'a':a}) == 2

    s = "a[0,0,0]"
    assert _test(e, s, 'eval', {'a':a}) == 3

log = []

def watch(*args):
    log.append(args)

def test2():
    m = Machine(verbose=False)
    m.add_callback('CALL_FUNCTION', watch)
    
    c = compile('def func1():\n  return 1\ndef func2():\n  return 1 + func1()', '<string>', 'exec')
    
    g = {}
    
    m.exec(c, g)
    
    # no functions called yet
    assert log == []
   
    f = g['func2']

    assert f() == 2
    
    # we get a callback for calling func1 but not func2 because func2 was directly
    # called, not called through the machine
    assert log == [(g['func1'],)]

def test_cmp_op_not_in():
    assert _test(None, "0 not in [0]", "eval") == False

def test_build_tuple():
    assert _test(None, "(0, 1)", "eval") == (0, 1)

def test_loop():
    s = """
for a in [0, 1]:
    continue
"""
    _test(None, s, "exec")




