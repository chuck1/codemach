import unittest
import types
import dis
import codemach
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
    #print('\nsource:\n{}\n'.format(s))
    c = compile(s, '<string>', mode)

    #code_info(c)

    return e.exec(c)

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
    e = Machine(logging.INFO)
    
    #log_config()
    
    s = """def func(a, b):\n  return a + b\nfunc(2, 3)"""
    _test(e, s, 'exec')
    

