import io
import sys
import dis
import types
import operator
import builtins
import pprint

import async_patterns

from .assembler import *

__all__ = ['Machine']

def function_wrapper(m, f):
    """
    Wrap a function so that when called, its code is executed by **machine**.

    :param machine: a :py:class:`Machine` object
    :param f: a python function object
    """
    def wrapped(*args):
        c = f.__code__

        l = {}

        varnames = list(c.co_varnames)
        
        m._print('wrapped')
        m._print(f)
        m._print(args)
        #self._print('callable = {}'.format(callable_))
        #self._print('closure  = {}'.format(callable_.function.__closure__))
        #self._print('args     = {}'.format(args))
        #self._print('varnames = {}'.format(varnames))

        args = list(args)
        for _ in range(c.co_argcount):
            l[varnames.pop(0)] = args.pop(0)
        
        if varnames:
            l[varnames.pop(0)] = tuple(args)

        return m.exec(f.__code__, f.__globals__, l)
    
    return wrapped

class FunctionType(object):
    def __init__(self, machine, code, globals_, name):
        self._machine = machine
        self.func_raw = types.FunctionType(code, globals_, name)
        self.function = function_wrapper(
                machine,
                self.func_raw)
        self.wrapped = self.function

    def get_code(self):
        """
        return the code object to be used by Machine
        """
        return self.function.__closure__[0].cell_contents.__code__
    
    def __repr__(self):
        return '<{} object, function={}>'.format(self.__class__.__module__+'.'+self.__class__.__name__, self.func_raw.__name__)

    def __call__(self, args):
        return self.wrapped(args)

class InstructionIterator:
    def __init__(self, inst):
        self._inst = list(inst)

        self._tab = dict((i.offset, (i, a)) for i, a in zip(self._inst, range(len(self._inst))))
    
    def __iter__(self):
        self._iter = iter(self._inst)
        return self

    def __next__(self):
        return next(self._iter)

    def jump(self, offset):
        i, a = self._tab[offset]

        self._iter = iter(self._inst)

        for _ in range(a):
            next(self._iter)

class Machine(object):
    """
    Class that executes python code objects.
    
    :param verbose: verbosity level
    """
    def __init__(self, verbose=False, callbacks={}):
        self.__stack = []
        self.__blocks = []

        self.verbose = verbose
        
        self.__callbacks = callbacks
        
        if not verbose:
            self._output = io.StringIO()
   
    def add_callback(self, opname, callable_):
        if opname not in self.__callbacks:
            self.__callbacks[opname] = async_patterns.Callbacks()
        self.__callbacks[opname].add_callback(callable_)

    def call_callbacks(self, opname, *args, **kwargs):
        if opname not in self.__callbacks: return
        self.__callbacks[opname](*args, **kwargs)

    def _print(self, *args):
        if self.verbose:
            print(*args)
        else:
            print(*args, file=self._output)

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

    def exec(self, code, globals_=None, _locals=None):
        """
        Execute a code object
        
        The inputs and behavior of this function should match those of
        eval_ and exec_.

        .. _eval: https://docs.python.org/3/library/functions.html?highlight=eval#eval
        .. _exec: https://docs.python.org/3/library/functions.html?highlight=exec#exec

        .. note:: Need to figure out how the internals of this function must change for
           ``eval`` or ``exec``.

        :param code: a python code object
        :param globals_: optional globals dictionary
        :param _locals: optional locals dictionary
        """
        if globals_ is None:
            globals_ = globals()
        if _locals is None:
            self._locals = globals_
        else:
            self._locals = _locals
       
        self.__globals = globals_
        

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
        self._print('build_class')
        self._print(callable_)
        self._print('args=',args)
        
        if isinstance(args[0], FunctionType):
            c = args[0].get_code()
        else:
            c = args[0].__closure__[0].cell_contents.__code__

        machine = Machine(self.verbose)
        l = dict()
        machine.exec(c, self.__globals, l)

        # construct code for class source
        a = Assembler()
        for name, value in l.items():
            a.load_const(value)
            a.store_name(name)
        a.load_const(None)
        a.return_value()
       
        machine = Machine(self.verbose)

        f = types.FunctionType(a.code(), self.__globals, args[1])

        args = (f, *args[1:])

        self.call_callbacks('CALL_FUNCTION', callable_, *args)
                 
        return callable_(*args)

    def call_function(self, i):
        """
        Implement the CALL_FUNCTION_ operation.

        .. _CALL_FUNCTION: https://docs.python.org/3/library/dis.html#opcode-CALL_FUNCTION
        """
        callable_ = self.__stack[-1-i.arg]
        
        args = tuple(self.__stack[len(self.__stack) - i.arg:])
 
        self.call_callbacks('CALL_FUNCTION', callable_, *args)
   
        if isinstance(callable_, types.CodeType):
            _c = callable_
            e = Machine(self.verbose)
            
            l = dict((name, arg) for name, arg in zip(
                _c.co_varnames[:_c.co_argcount], args))
            
            ret = e.exec(c, self.__globals, l)
        elif isinstance(callable_, FunctionType):
            
            if False:
                c = callable_.get_code()
                m = callable_._machine
                
                # construct locals
                l = {}
                varnames = list(c.co_varnames)
                
                self._print('callable = {}'.format(callable_))
                self._print('closure  = {}'.format(callable_.function.__closure__))
                self._print('args     = {}'.format(args))
                self._print('varnames = {}'.format(varnames))
    
                args = list(args)
                for _ in range(c.co_argcount):
                    l[varnames.pop(0)] = args.pop(0)
                
                if varnames:
                    l[varnames.pop(0)] = tuple(args)
    
                ret = m.exec(c, self.__globals, l)
            else:
                ret = callable_(args)

        elif (callable_ is builtins.__build_class__) and isinstance(args[0], FunctionType):
            ret = self.build_class(callable_, args)
        
        elif callable_ is builtins.__build_class__:
            ret = self.build_class(callable_, args)

        else:
            ret = callable_(*args)
        
        self.pop(1 + i.arg)
        self.__stack.append(ret)
    
    def __build_list(self, i):
        self.__stack.append(list(self.pop(i.arg)))

    def __inst_setup_loop(self, i):
        self.__blocks.append(i.arg)
    
    def __inst_get_iter(self, i):
        self.__stack.append(iter(self.__stack.pop()))

    def __inst_for_iter(self, i):
        TOS = self.__stack[-1]
        
        try:
            self.__stack.append(TOS.__next__())
        except StopIteration:
            self.__stack.pop()
            self._ii.jump(i.arg + i.offset + 2)

    def __inst_jump_absolute(self, i):
        self._ii.jump(i.arg)

    def __inst_pop_block(self, i):
        self.__blocks.pop()

    def __inst_pop_jump_if_true(self, i):
        if self.__stack.pop():
            self._ii.jump(i.arg)

    def __inst_unpack_sequence(self, i):
        TOS = self.__stack.pop()
        for el in reversed(TOS):
            self.__stack.append(el)

    def __inst_raise_varargs(self, i):
        cls = self.__stack.pop()
        args = self.pop(i.arg-1)
        raise cls(*args)

    def exec_instructions(self, c):

        self._print('------------- begin exec')
        
        inst = dis.Bytecode(c)
        
        return_value_set = False
        
        self._ii = InstructionIterator(inst)

        if self.verbose:
            pprint.pprint(self._ii._tab)

        ops = {
                'BUILD_LIST': self.__build_list,
                'CALL_FUNCTION': self.call_function,
                'SETUP_LOOP': self.__inst_setup_loop,
                'GET_ITER': self.__inst_get_iter,
                'FOR_ITER': self.__inst_for_iter,
                'JUMP_ABSOLUTE': self.__inst_jump_absolute,
                'POP_BLOCK': self.__inst_pop_block,
                'POP_JUMP_IF_TRUE': self.__inst_pop_jump_if_true,
                'UNPACK_SEQUENCE': self.__inst_unpack_sequence,
                'RAISE_VARARGS': self.__inst_raise_varargs,
                }
        
        #for i in inst:
        for i in self._ii:
            
            if return_value_set:
                raise RuntimeError('RETURN_VALUE is not last opcode')
            
            if i.opname in ops:
                try:
                    
                    ops[i.opname](i)
                    
                except Exception as e:
                    print('during machine exec {}: {}'.format(i.opname, e))
                    if not self.verbose:
                        print('printing output')
                        print(self._output.getvalue())
                    raise
 
            elif i.opcode == 1:
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
                
                self.call_callbacks('LOAD_ATTR', o, name)

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

                self.call_callbacks('IMPORT_NAME', c.co_names[i.arg], TOS, TOS1)

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


            elif i.opcode == 132:
                # MAKE_FUNCTION
                if i.arg != 0:
                    raise RuntimeError('not yet supported')
                
                n = dis.stack_effect(i.opcode, i.arg)
                args = self.pop(-n)

                code = self.__stack.pop()
                
                f = FunctionType(Machine(self.verbose), code, self.__globals, args[0])
                
                # experimenting
                f = f.wrapped

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
    
            self._print('{:20} {}'.format(i.opname, [(repr(s) if not str(hex(id(s))) in repr(s) else s.__class__) for s in self.__stack ]))
    
        self._print('------------- return')

        return return_value
        

