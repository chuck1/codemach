#!/usr/bin/env python3

import sys
import dis
import types

import executor



def inst_to_bytes(inst):
    if inst.opcode in (100, 101, ):
        return bytes([
            inst.opcode,
            inst.arg,
            0])
    elif inst.opcode in (23, 83):
        return bytes([inst.opcode])
    else:
        raise RuntimeError()

class Inst(object):
    def __init__(self):
        self.offset = 0
        self.insts = list()
        self.consts = list()
        self.names = list()
        self.varnames = list()

    def get_const_arg(self, v):
        if not v in self.consts:
            self.consts.append(v)
        return self.consts.index(v)

    def load_const(self, argval):
        inst = dis.Instruction(
                'LOAD_CONST',
                dis.opname.index('LOAD_CONST'),
                self.get_const_arg(argval),
                argval,
                repr(argval),
                self.offset,
                None,
                False)
        
        self.offset += 3
        
        self.insts.append(inst)

    def binary_add(self):
        inst = dis.Instruction(
                'BINARY_ADD',
                dis.opname.index('BINARY_ADD'),
                None,
                None,
                '',
                self.offset,
                None,
                False)
        
        self.offset += 1
        
        self.insts.append(inst)

    def return_value(self):
        inst = dis.Instruction(
                'RETURN_VALUE',
                dis.opname.index('RETURN_VALUE'),
                None,
                None,
                '',
                self.offset,
                None,
                False)
        
        self.offset += 1
        
        self.insts.append(inst)

    def code(self):

        b = b''.join(inst_to_bytes(i) for i in self.insts)
        print('bytes',b)

        c = types.CodeType(
                0,
                0,
                0,
                2,
                64,
                b,
                tuple(self.consts),
                tuple(self.names),
                tuple(self.varnames),
                '<constructed code>',
                '<module>',
                0,
                b'')

        return c

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


intp = Interpreter()

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
  
    ret = intp.exec(c)
    print('return:',ret)
    print()

 
def test1(): 
    
    s = """
    a = 5
    c = 1 + a
    """
    
    analyze(s)
    
    insts = Inst()
    
    insts.load_const(2)
    insts.load_const(3)
    insts.binary_add()
    insts.return_value()
    
    print_insts(insts.insts)
    
    c = insts.code()
    
    print(c)
    
    print('eval')
    print(eval(c))
    
s = """
object.__getattribute__(foo, 'secret')
"""

analyze(s)

sys.exit(0)

s = """
def func(a, b):
    return getattr(a, b)
func(object, '__getattribute__')
"""

s = """
object.__getattribute__
"""
 
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









