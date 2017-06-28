__version__ = '0.3b14'

import sys
import dis
import types
import operator
import builtins

"""
CodeMach
========

This module was created to solve the security issues
associated with execution of arbitrary code strings.
The Machine class can execute python code objects
and allow the user to intervene.

Handling class method code
--------------------------

The builtin function __build_class__ requires a function
object containing the source code of the class.
If we simple pass this function, it will not be executed
by the machine, but rather by the default implementation.
The solution is to pass a function wrapper the within the
wrapper allow the Machine to execute the actual function
and return the result.

http://grokbase.com/t/python/python-list/033r5nks47/type-function-does-not-subtype#20030324rcnwbkfedhzbaf3vmiuer3z4xq

Operations
----------

140 CALL_FUNCTION_VAR

need more testing, but in one test, was used to call a function defined as
:

    def foo(*args):
        pass

where TOS1 is the function object and TOS is a tuple of arguments


"""

class Signal(object):
    def __init__(self):
        self.__watch = None

    def emmit(self, *args):
        if self.__watch is not None:
            self.__watch(*args)

    def subscribe(self, callback):
        self.__watch = callback

    def unsubscribe(self):
        self.__watch = None

class CodeType(object):
    def __init__(self, code):
        self.code = code

class FunctionCall(object):
    pass

def function_wrapper(machine, f):
    def wrapper(*args):
        print('wrapper\n{} {}\ncalled with {}'.format(f, machine, args))

        return machine.exec(f.__code__, f.__globals__)
        #return f(*args)
    
    return wrapper

def function_wrapper_class_source(machine, f):
    def wrapper(*args):
        print('wrapper\n{} {}\ncalled with {}'.format(f, machine, args))

        res = machine.exec(f.__code__, f.__globals__)

        print('globals after running class source')
        for k, v in f.__globals__.items():
            print('  {}'.format(k))

        return res
        #return f(*args)
    
    return wrapper

class FunctionType(object):
    def __init__(self, machine, code, globals_, name):
        self.func_raw = types.FunctionType(code, globals_, name)
        self.function = function_wrapper(
                machine,
                self.func_raw)

    def get_code(self):
        """
        return the code object to be used by Machine
        """
        print('closures')
        print(self.function.__closure__)
        return self.function.__closure__[0].cell_contents.__code__

    def get_function(self, machine):
        """
        return the function object to be passed to builtin.__build_class__
        """
        #return self.function
        return function_wrapper(
                machine,
                self.func_raw)

    def get_function_as_class_source(self, machine):
        return function_wrapper_class_source(
                machine,
                self.func_raw)


    def __repr__(self):
        return '<{} object, function {}>'.format(self.__class__.__name__, self.func_raw)

class SignalThing(object):
    def __init__(self):
        self.__watch = {}

    def emmit(self, thing, *args):
        try:
            if thing in self.__watch:
                self.__watch[thing](thing, *args)
        except TypeError:
            pass

    def subscribe(self, thing, callback):
        self.__watch[thing] = callback

    def unsubscribe(self, thing):
        del self.__watch[thing]
   

class Machine(object):
    def __init__(self, verbose=0):
        self.__stack = []
        self.verbose = verbose
        
        self.signal = {
                'IMPORT_NAME': Signal(),
                'CALL_FUNCTION': SignalThing(),
                'LOAD_ATTR': SignalThing(),
                }

    @staticmethod
    def cmp_op(i):
        def not_in(a, b):
            return not (a in b)
        return (
                operator.lt, 
                operator.le, 
                operator.eq, 
                operator.ne, 
                operator.gt, 
                operator.ge, 
                operator.contains, 
                not_in, 
                operator.is_, 
                operator.is_not, 
                'exception match', 
                'BAD')[i]

    def exec(self, code, _globals=globals(), _locals=None):
        if _locals is None:
            self._locals = _globals
        else:
            self._locals = _locals
       
        self.__globals = _globals

        return self.exec_instructions(code)

    def load_name(self, name):
        if name in self.__globals:
            return self.__globals[name]
        
        b = self.__globals['__builtins__']
        if isinstance(b, dict):
            return b[name]
        else:
            return getattr(b, name)

    def store_name(self, name, val):
        print('%20s' % 'STORE_NAME', val, '->', name)
        self._locals[name] = val
        #self.__globals[name] = val

    def pop(self, n):
        poped = self.__stack[len(self.__stack) - n:]
        del self.__stack[len(self.__stack) - n:]
        return poped
        
    def build_class(self, callable_, args):
        print('build class', args)
    
        machine = Machine(self.verbose)
        l = dict()
        machine.exec(args[0].get_code(), self.__globals, l)
        print('l=', l)

        # construct code for class source
        a = Assembler()
        for name, value in l.items():
            a.load_const(value)
            a.store_name(name)
        a.load_const(None)
        a.return_value()
       
        #machine = Machine(self.verbose)
        machine = MachineClassSource(self.verbose)

        #args = (args[0].get_function_as_class_source(machine), *args[1:])

        f = types.FunctionType(a.code(), self.__globals, args[1])

        args = (f, *args[1:])

        self.signal['CALL_FUNCTION'].emmit(callable_, *args)
                 
        return callable_(*args)

    
    def exec_instructions(self, c):

        if self.verbose > 0:
            print('------------- begin exec')
            print('  locals =', self._locals.keys())
        
        inst = dis.Bytecode(c)
        
        return_value_set = False
    
        for i in inst:

            if return_value_set:
                raise RuntimeError('RETURN_VALUE is not last opcode')
    
            #print('se',dis.stack_effect(i.opcode, i.arg))
            if i.opcode == 1:
                self.__stack.pop()

            elif i.opcode == 10:
                # UNARY_POSITIVE
                TOS = self.__stack.pop()
                self.__stack.append(+TOS)

            elif i.opcode == 11:
                # UNARY_NEGATIVE
                TOS = self.__stack.pop()
                self.__stack.append(-TOS)

            elif i.opcode == 19:
                # BINARY_POWER
                TOS = self.__stack.pop()
                TOS1 = self.__stack.pop()
                self.__stack.append(TOS1 ** TOS)

            elif i.opcode == 22:
                # BINARY_MODULO
                TOS = self.__stack.pop()
                TOS1 = self.__stack.pop()
                self.__stack.append(TOS1 % TOS)

            elif i.opcode == 23:
                # BINARY_ADD
                TOS = self.__stack.pop()
                TOS1 = self.__stack.pop()
                self.__stack.append(TOS1 + TOS)

            elif i.opcode == 24:
                # BINARY_SUBTRACT
                TOS = self.__stack.pop()
                TOS1 = self.__stack.pop()
                self.__stack.append(TOS1 - TOS)

            elif i.opcode == 25:
                # BINARY_SUBSCR
                TOS = self.__stack.pop()
                TOS1 = self.__stack.pop()
                self.__stack.append(TOS1[TOS])

            elif i.opcode == 26:
                # BINARY_FLOOR_DIVIDE
                TOS = self.__stack.pop()
                TOS1 = self.__stack.pop()
                self.__stack.append(TOS1 // TOS)

            elif i.opcode == 27:
                # BINARY_TRUE_DIVIDE
                TOS = self.__stack.pop()
                TOS1 = self.__stack.pop()
                self.__stack.append(TOS1 / TOS)

            elif i.opcode == 71:
                # LOAD_BUILD_CLASS
                self.__stack.append(builtins.__build_class__)

            elif i.opcode == 83:
                # RETURN_VALUE
                return_value = self.__stack.pop()
                return_value_set = True

            elif i.opcode == 90:
                # STORE_NAME
                name = c.co_names[i.arg]
                TOS = self.__stack.pop()
                self.store_name(name, TOS)

            elif i.opcode == 100:
                # LOAD_CONST
                self.__stack.append(c.co_consts[i.arg])

            elif i.opcode == 101:
                # LOAD_NAME
                name = c.co_names[i.arg]
                self.__stack.append(self.load_name(name))

            elif i.opcode == 102:
                # BUILD_TUPLE
                self.__stack.append(tuple(self.pop(i.arg)))

            elif i.opcode == 106:
                # LOAD_ATTR
                name = c.co_names[i.arg]
                o = self.__stack.pop()
                
                self.signal['LOAD_ATTR'].emmit(o, name)

                self.__stack.append(getattr(o, name))
            
            elif i.opcode == 107:
                # COMPARE_OP
                TOS = self.__stack.pop()
                TOS1 = self.__stack.pop()
                self.__stack.append(Machine.cmp_op(i.arg)(TOS1, TOS))

            elif i.opcode == 108:
                # IMPORT_NAME
                TOS = self.__stack.pop()
                TOS1 = self.__stack.pop()

                self.signal['IMPORT_NAME'].emmit(c.co_names[i.arg], TOS, TOS1)

                self.__stack.append(__import__(c.co_names[i.arg], fromlist=TOS, level=TOS1))

            elif i.opcode == 116:
                # LOAD_GLOBAL
                name = c.co_names[i.arg]
                self.__stack.append(self.load_name(name))

            elif i.opcode == 124:
                # LOAD_FAST:
                name = c.co_varnames[i.arg]
                self.__stack.append(self._locals[name])
    
            elif i.opcode == 125:
                # STORE_FAST
                TOS = self.__stack.pop()
                name = c.co_varnames[i.arg]
                self._locals[name] = TOS

            elif i.opcode == 131:
                # CALL_FUNCTION
                callable_ = self.__stack[-1-i.arg]
                
                args = tuple(self.__stack[len(self.__stack) - i.arg:])
    
                if isinstance(callable_, types.CodeType):
                    _c = callable_
                    e = Machine(self.verbose)
                    
                    l = dict((name, arg) for name, arg in zip(
                        _c.co_varnames[:_c.co_argcount], args))
                    
                    ret = e.exec(_c, self.__globals, l)
                elif isinstance(callable_, FunctionType):
                    _c = callable_.get_code()
                    e = Machine(self.verbose)
                    
                    e._locals = dict((name, arg) for name, arg in zip(
                        _c.co_varnames[:_c.co_argcount], args))
                    l = dict((name, arg) for name, arg in zip(
                        _c.co_varnames[:_c.co_argcount], args))
                    
                    ret = e.exec(_c, self.__globals, l)
                elif (callable_ is builtins.__build_class__) and isinstance(args[0], FunctionType):
                    ret = self.build_class(callable_, args)
                else:
                    self.signal['CALL_FUNCTION'].emmit(callable_, *args)

                    ret = callable_(*args)
                
                self.pop(1 + i.arg)
                self.__stack.append(ret)

            elif i.opcode == 132:
                # MAKE_FUNCTION
                if i.arg != 0:
                    raise RuntimeError('not yet supported')
                
                #print(i.opname, i.opcode, i.arg, dis.stack_effect(i.opcode, i.arg))
                n = dis.stack_effect(i.opcode, i.arg)
                args = self.pop(-n)

                code = self.__stack.pop()
                f = FunctionType(Machine(self.verbose), code, self.__globals, args[0])
                self.__stack.append(f)

                print('MAKE_FUNCTION')
                print('throwing away:', args)
                print('f.__qualname__:', f.func_raw.__qualname__)

            elif i.opcode == 133:
                # BUILD_SLICE
                TOS = self.__stack.pop()
                TOS1 = self.__stack.pop()
                if i.arg == 2:
                    self.__stack.append(slice(TOS1, TOS))
                else:
                    TOS2 = self.__stack.pop()
                    self.__stack.append(slice(TOS2, TOS1, TOS))
                
            else:
                raise RuntimeError('unhandled opcode',i.opcode,i.opname,i.arg,self.__stack)
    
            if self.verbose > 0:
                print('%20s' % i.opname, self.__stack)
    
        if self.verbose > 0:print('------------- return')
        return return_value
        
class MachineClassSource(Machine):
    def store_name(self, name, val):
        Machine.store_name(self, name, val)
        print(self.__class__.__name__, 'store_name', name, val)

def inst_to_bytes(inst):
    if inst.opname in (
            'LOAD_CONST',
            'LOAD_NAME',
            'STORE_NAME',
            ):
        return bytes([
            inst.opcode,
            inst.arg,
            0])
    elif inst.opname in (
            'BINARY_ADD',
            'RETURN_VALUE',
            ):
        return bytes([inst.opcode])
    else:
        raise RuntimeError('unsupported op {}'.format(inst.opname))

class Assembler(object):
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

    def get_name_arg(self, v):
        if not v in self.names:
            self.names.append(v)
        return self.names.index(v)

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

    def load_name(self, argval):
        inst = dis.Instruction(
                'LOAD_NAME',
                dis.opname.index('LOAD_NAME'),
                self.get_name_arg(argval),
                argval,
                repr(argval),
                self.offset,
                None,
                False)
        
        self.offset += 3
        
        self.insts.append(inst)

    def store_name(self, argval):
        inst = dis.Instruction(
                'STORE_NAME',
                dis.opname.index('STORE_NAME'),
                self.get_name_arg(argval),
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


 
def test1():
 
    asm = Assembler()
    
    asm.load_const(2)
    asm.load_const(3)
    asm.binary_add()
    asm.return_value()
    
    print_asm(insts.insts)
    
    c = asm.code()
    
    print(c)
    
    print('eval')
    print(eval(c))
    

