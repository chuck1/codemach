import unittest
import types
import dis
from codemach import Machine
import logging.config


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
    print('\nsource:\n{}\n'.format(s))
    c = compile(s, '<string>', mode)

    code_info(c)

    print(e.exec(c))
    print()

def log_config():
    logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': True,
    'handlers': {
        'console':{
            'level':'DEBUG',
            'class':'logging.StreamHandler',
            'formatter': 'basic'
            },
        },
    'loggers':{
        'codemach': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
            },
        '__main__': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
            },
        },
    'formatters': {
        "basic":{
            "format":"%(asctime)s %(process)s %(module)10s %(funcName)16s %(levelname)7s %(message)s"
            }
        }
    })

def test_mach():
    e = Machine()
    e.verbose = 1

    log_config()
    
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


