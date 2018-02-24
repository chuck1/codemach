#!/usr/bin/env python3

import sys
import dis
import types

from codemach.machine import Machine
from codemach.assembler import Assembler

def print_code(c):
    print('argcount      ',c.co_argcount)
    print('kwonlyargcount',c.co_kwonlyargcount)
    print('nlocals       ',c.co_argcount)
    print('stacksize     ',c.co_stacksize)
    print('flags         ',c.co_flags)
    print('codestring    ',c.co_code)
    print('constants     ',c.co_consts)
    print('names         ',c.co_names)
    print('varnames      ',c.co_varnames)
    print('filename      ',c.co_filename)
    print('name          ',c.co_name)
    print('firstlineno   ',c.co_firstlineno)
    print('lnotab        ',c.co_lnotab)
    
"""
argcount, kwonlyargcount, nlocals, stacksize, flags, codestring,
|        constants, names, varnames, filename, name, firstlineno,
  |        lnotab[, freevars[, cellvars]])
"""

def print_insts(inst):
    fmt = "{:14s}"+"{:10s}"*6
    print(fmt.format(
            'opname',
            'opcode',
            'arg',
            'argval',
            #'argrepr',
            'offset',
            'sl',
            'ijt'))
    
    for i in inst:
        #print(i.opname, repr(i.argval), type(i.argval), repr(i.argval.__class__.__name__))
        print(fmt.format(i.opname, *(str(a)[:9] for a in (
            i.opcode,
            i.arg,
            i.argval,
            #i.argrepr,
            i.offset,
            i.starts_line,
            i.is_jump_target))))
        
        if i.argval.__class__.__name__ == 'code':
            c = i.argval
            
            print('>>>>>>>>')
            print_insts(dis.Bytecode(c))
            print('<<<<<<<<')

class Foo(object):
    secret = 'hello'

foo = Foo()

def analyze(s):
    print('=================================')
    c = compile(s, '<string>', 'exec')

    print_code(c)
  
    #for x in c.co_code: print("{:02x}".format(x))
    print(' '.join([str(x) for x in c.co_code]))
    
    dis.dis(c)
    
    inst = dis.Bytecode(c)
        
    print_insts(inst)
   
    print('stack')
    
    m = Machine(c, verbose=True)
    ret = m.execute()
    print('return:',ret)
    print()
 
def test1(): 
    s = "a = 5\nc = 1 + a"
    analyze(s)
    
    a = Assembler()
    
    a.load_const(2)
    a.load_const(3)
    a.binary_add()
    a.return_value()
    
    print_insts(a.insts)
    
    c = a.code()
    
    print(c)
    
    print('eval')
    print(eval(c))

def test2():
    
    #s = "object.__getattribute__(foo, 'secret')"
    #analyze(s)
    
    s = "def func(a, b):\n  return getattr(a, b)\nfunc(object, '__getattribute__')"   
    analyze(s)

    s = "object.__getattribute__"
    analyze(s)
    
    s = """
def func1(b, c):
    return getattr(b, c)
def func(a):
    return func1(object, a)
print(func('__getattribute__'))
"""
    
    analyze(s)
    
    s = """
def func(a, b, c):
    return a + b + c
c = 1 + func(2, 3, 4)
"""
    
    analyze(s)









