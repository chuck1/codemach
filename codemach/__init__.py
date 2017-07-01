__version__ = '0.4b1'

import sys
import dis
import types
import operator
import builtins
import logging
import logging.config

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

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
    """
    Wrap a function so that when called, its code is executed by **machine**.

    :param machine: a :py:class:`Machine` object
    :param f: a python function object
    """
    def wrapper(*args):
        logger.debug('wrapper {}'.format(f))
        logger.debug('called with {}'.format(args))

        return machine.exec(f.__code__, f.__globals__)
    
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
        logger.debug('closures')
        logger.debug(self.function.__closure__)
        return self.function.__closure__[0].cell_contents.__code__
    
    def function_wrapped(self, machine):
        """
        return the function object to be passed to builtin.__build_class__
        """
        #return self.function
        return function_wrapper(
                machine,
                self.func_raw)

    def __repr__(self):
        return '<{} object, function={}>'.format(self.__class__.__module__+'.'+self.__class__.__name__, self.func_raw.__name__)

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
    """
    Class that executes python code objects.
    
    :param verbose: verbosity level
    """
    def __init__(self, verbose=False):
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

    def exec(self, code, _globals=None, _locals=None):
        """
        Execute a code object
        
        The inputs and behavior of this function should match those of
        eval_ and exec_.

        .. _eval: https://docs.python.org/3/library/functions.html?highlight=eval#eval
        .. _exec: https://docs.python.org/3/library/functions.html?highlight=exec#exec

        .. note:: Need to figure out how the internals of this function must change for
           ``eval`` or ``exec``.

        :param code: a python code object
        :param _globals: optional globals dictionary
        :param _locals: optional locals dictionary
        """
        if _globals is None:
            _globals = globals()
        if _locals is None:
            self._locals = _globals
        else:
            self._locals = _locals
       
        self.__globals = _globals

        return self.exec_instructions(code)

    def load_name(self, name):
        """
        Implementation of the LOAD_NAME operation
        """
        if name in self.__globals:
            return self.__globals[name]
        
        b = self.__globals['__builtins__']
        if isinstance(b, dict):
            return b[name]
        else:
            return getattr(b, name)

    def store_name(self, name, val):
        """
        Implementation of the STORE_NAME operation
        """
        logging.debug('{:20} {} -> {}'.format('STORE_NAME', val, name))
        self._locals[name] = val
        #self.__globals[name] = val

    def pop(self, n):
        """
        Pop the **n** topmost items from the stack and return them as a ``list``.
        """
        poped = self.__stack[len(self.__stack) - n:]
        del self.__stack[len(self.__stack) - n:]
        return poped
        
    def build_class(self, callable_, args):
        """
        Implement ``builtins.__build_class__``.
        We must wrap all class member functions using :py:func:`function_wrapper`.
        This requires using a :py:class:`Machine` to execute the class source code
        and then recreating the class source code using an :py:class:`Assembler`.

        .. note: We might be able to bypass the call to ``builtins.__build_class__``
           entirely and manually construct a class object.
        """
    
        machine = Machine(self.verbose)
        l = dict()
        machine.exec(args[0].get_code(), self.__globals, l)

        # construct code for class source
        a = Assembler()
        for name, value in l.items():
            a.load_const(value)
            a.store_name(name)
        a.load_const(None)
        a.return_value()
       
        #machine = Machine(self.verbose)
        machine = MachineClassSource(self.verbose)

        f = types.FunctionType(a.code(), self.__globals, args[1])

        args = (f, *args[1:])

        self.signal['CALL_FUNCTION'].emmit(callable_, *args)
                 
        return callable_(*args)

    def call_function(self, i):
        """
        Implement the CALL_FUNCTION_ operation.

        .. _CALL_FUNCTION: https://docs.python.org/3/library/dis.html#opcode-CALL_FUNCTION
        """
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
    
    def exec_instructions(self, c):

        if self.verbose:
            print('------------- begin exec')
        
        inst = dis.Bytecode(c)
        
        return_value_set = False
    
        for i in inst:

            if return_value_set:
                raise RuntimeError('RETURN_VALUE is not last opcode')
    
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
                self.call_function(i)

            elif i.opcode == 132:
                # MAKE_FUNCTION
                if i.arg != 0:
                    raise RuntimeError('not yet supported')
                
                n = dis.stack_effect(i.opcode, i.arg)
                args = self.pop(-n)

                code = self.__stack.pop()
                f = FunctionType(Machine(self.verbose), code, self.__globals, args[0])
                self.__stack.append(f)

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
    
            if self.verbose:
                print('{:20} {}'.format(i.opname, [(repr(s) if not str(hex(id(s))) in repr(s) else s.__class__) for s in self.__stack ]))
    
        if self.verbose:
            print('------------- return')
        return return_value
        
class MachineClassSource(Machine):
    def store_name(self, name, val):
        Machine.store_name(self, name, val)
        logger.debug('{} {} {} {}'.format(self.__class__.__name__, 'store_name', name, val))

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
        logger.debug('bytes={}'.format(b))

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


 
   

