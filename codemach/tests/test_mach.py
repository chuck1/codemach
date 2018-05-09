import os
import types
import dis
from pprint import pprint
import pytest
import codemach
import codemach.machine
from codemach.machine import Machine


def _test(_, s, mode, globals_=None):
    #print('\nsource:\n{}\n'.format(s))
    c = compile(s, '<string>', mode)

    m = Machine(c, verbose=True)

    codemach.machine.code_info(c)

    return m.execute(globals_=globals_)

def end_format_value_0x5(m):
    assert m.globals_['b'] == '1 '

@pytest.mark.parametrize("filename,inst,end", [
    ("comp_equal.py", ("COMPARE_OP", 2), None),
    ("import.py", ("IMPORT_NAME", None), None),
    ("binary_floor_divide.py", ("BINARY_FLOOR_DIVIDE", None), None),
    ("binary_modulo.py", ("BINARY_MODULO", None), None),
    ("binary_power.py", ("BINARY_POWER", None), None),
    ("binary_true_divide.py", ("BINARY_TRUE_DIVIDE", None), None),
    (
        "binary_multiply.py",
        ("BINARY_MULTIPLY", None),
        None),
    (
        "binary_subtract.py",
        ("BINARY_SUBTRACT", None),
        None),
    (
        "binary_matrix_multiply.py",
        ("BINARY_MATRIX_MULTIPLY", None),
        None),
    ("build_tuple.py", ("BUILD_TUPLE", None), None),
    ("format_value.py", ("FORMAT_VALUE", 0x0), None),
    ("format_value_0x1.py", ("FORMAT_VALUE", 0x1), None),
    ("format_value_0x2.py", ("FORMAT_VALUE", 0x2), None),
    ("format_value_0x4.py", ("FORMAT_VALUE", 0x4), None),
    ("format_value_0x5.py", ("FORMAT_VALUE", 0x5), end_format_value_0x5),
    ("raise_varargs.py", ("RAISE_VARARGS", None), None),
    ("unary_negative.py", ("UNARY_NEGATIVE", None), None),
    ("unary_positive.py", ("UNARY_POSITIVE", None), None),
    ("yield.py", ("YIELD_VALUE", None), None),
    (
        "function_0.py",
        ("MAKE_FUNCTION", None),
        None),
    (
        "function_1.py",
        ("MAKE_FUNCTION", None),
        None),
    (
        "function_2.py",
        ("MAKE_FUNCTION", None),
        None),
    (
        "load_attr_0.py",
        ("LOAD_METHOD", None),
        None),
    (
        "class_function.py",
        ("LOAD_BUILD_CLASS", None),
        None),
    (
        "build_slice_0x0.py",
        ("BUILD_SLICE", None),
        None),
    (
        "loop_0x0.py",
        ("SETUP_LOOP", None),
        None),
    (
        "unpack.py",
        ("UNPACK_SEQUENCE", None),
        None),
    (
        "globals.py",
        ("STORE_NAME", None),
        None),
    ])
def test_from_file(filename, inst, end):
    print(filename, inst, end)
    d = os.path.dirname(__file__)
    with open(os.path.join(d, "source", filename)) as f:
        s = f.read()
    
    c = compile(s, '<string>', 'exec')

    m = Machine(c, verbose=True)

    print('code:')
    print(s)
    print()

    codemach.machine.code_info(c)
    
    try:
        m.execute()
    except Exception as e:
        print(e)
        print(repr(e))
        print(dir(e))
        print(e.args)
        print(e.args[4])
        raise

    for i in m.inst_history:
        print(i)
    
    assert m.contains_op_history(inst)

    if end:
        end(m)

def test_mach():
    e = None
    
    s = """import math\ndef func():\n  return math.pi\nfunc()"""
    _test(e, s, 'exec')

    s = """import datetime\ndatetime.datetime.now()"""
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

    s = "a[0,0]"
    assert _test(e, s, 'eval', {'a':a}) == 2

    s = "a[0,0,0]"
    assert _test(e, s, 'eval', {'a':a}) == 3

log = []

def watch(*args):
    log.append(args)

def test2():
    # Test getting objects created by the executed code.
    # Test callbacks.

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





