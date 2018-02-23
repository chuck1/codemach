import os
import types
import dis
import pytest
import codemach
from codemach.machine import Machine

def code_info(c):
    print('------------')
    print('argcount         ',c.co_argcount)
    print('consts           ',c.co_consts)
    print('names            ',c.co_names)
    print('varnames         ',c.co_varnames)
    print('co_cellvars      ', c.co_cellvars)
    print('co_flags         ', c.co_flags)
    print('co_freevars      ', c.co_freevars)
    print('co_kwonlyargcount', c.co_kwonlyargcount)
    print('co_lnotab        ', c.co_lnotab)
    print('co_name          ', c.co_name)
    print('co_nlocals       ', c.co_nlocals)
    print('co_stacksize     ', c.co_stacksize)
    dis.dis(c)
    print('------------')
    for const in c.co_consts:
        if isinstance(const, types.CodeType):
            code_info(const)

def _test(_, s, mode, globals_=None):
    #print('\nsource:\n{}\n'.format(s))
    c = compile(s, '<string>', mode)

    m = Machine(c, verbose=True)

    code_info(c)

    return m.execute(globals_=globals_)

@pytest.mark.parametrize("filename,inst", [
    ("comp_equal.py", ("COMPARE_OP", 2)),
    ("import.py", ("IMPORT_NAME", None)),
    ("binary_floor_divide.py", ("BINARY_FLOOR_DIVIDE", None)),
    ("binary_modulo.py", ("BINARY_MODULO", None)),
    ("binary_power.py", ("BINARY_POWER", None)),
    ("binary_true_divide.py", ("BINARY_TRUE_DIVIDE", None)),
    ("unary_negative.py", ("UNARY_NEGATIVE", None)),
    ("unary_positive.py", ("UNARY_POSITIVE", None)),
    ("yield.py", ("YIELD_VALUE", None)),
    ])
def test_from_file(filename, inst):
    with open(os.path.join("codemach/tests/source", filename)) as f:
        s = f.read()
    
    c = compile(s, '<string>', 'exec')

    m = Machine(c, verbose=True)

    code_info(c)
    
    m.execute()

    for i in m.inst_history:
        print(i)
    
    assert m.contains_op_history(inst)

def test_mach():
    e = None

    s = """def func(a, b):\n  c = 4\n  return a + b + c\nfunc(2, 3)"""
    _test(e, s, 'exec')
    
    s = """object.__getattribute__(object, '__class__')"""
    _test(e, s, 'eval')
    
    s = """c = 4\ndef func():\n  a = 2\n  b = 3\n  return a + b + c\nfunc()"""
    _test(e, s, 'exec')

    s = """import math\ndef func():\n  return math.pi\nfunc()"""
    _test(e, s, 'exec')

    s = """import datetime\ndatetime.datetime.now()"""
    _test(e, s, 'exec')

    s = """x = 1\ny = 1\nx * y\nx - y\n\n"""
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
    
    c = compile('def func1():\n  return 1\ndef func2():\n  return 1 + func1()', '<string>', 'exec')
 
    m = Machine(c, verbose=False)

    m.add_callback('CALL_FUNCTION', watch)
   
    g = {}
    
    m.execute(g)
    
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

def test_func_args():
    s = """
def func(*args):
    return args
assert func(1, 2) == (1, 2)
"""
    _test(None, s, "exec")

def test_class1():
    s = """
class Foo(object):
    a = 1
foo = Foo()
"""
    _test(None, s, 'exec')

def test_class2():
    s = """
class Foo(object):
    def func(self):
        return 0
foo = Foo()
assert foo.func() == 0
"""
    _test(None, s, 'exec')

def test_unpack():
    s = """
a, b, c = (1, 2, 3)
assert a == 1
assert b == 2
assert c == 3
"""
    _test(None, s, 'exec')

def _test_yield():
    s = """
def f():
    yield 1
next(iter(f()))
"""
    _test(None, s, 'exec')
    

