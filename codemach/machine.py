import io
import sys
import dis
import types
import operator
import builtins
from pprint import pprint

import async_patterns

from .assembler import *

__all__ = ['Machine']

class FunctionType(object):
    def __init__(self, machine, code, globals_, name):
        self._machine = machine
        self.code = code
        self.func_raw = types.FunctionType(code, globals_, name)

    def get_code(self):
        """
        return the code object to be used by Machine
        """
        return self.code
    
    def __repr__(self):
        return '<{} object, function={}>'.format(self.__class__.__module__+'.'+self.__class__.__name__, self.func_raw.__name__)

    def __call__(self, *args):

        m = self._machine
        c = self.func_raw.__code__
        f = self.func_raw

        l = {}

        varnames = list(c.co_varnames)
            
        print(m.verbose)
        m._print('wrapped')
        m._print('self         ', self.__class__)
        m._print('f            ', f)
        m._print('args         ', args)
        m._print('c.co_argcount', c.co_argcount)
        m._print('varnames     ', varnames)
        #self._print('callable = {}'.format(callable_))
        #self._print('closure  = {}'.format(callable_.function.__closure__))
        #self._print('args     = {}'.format(args))
        #self._print('varnames = {}'.format(varnames))

        args = self.build_args(args)

        for _ in range(c.co_argcount):
            l[varnames.pop(0)] = args.pop(0)
        
        if varnames:
            l[varnames.pop(0)] = tuple(args)

        return m.execute(f.__globals__, l)

        #return self.wrapped(args)

    def build_args(self, args):
        return list(args)

class FunctionTypeClassFunction(FunctionType):
    def build_args(self, args):
        return [self.object] + list(args)
        
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

    def __init__(self, code, verbose=False, callbacks={}):
        self.code = code
        self.instructions = dis.Bytecode(self.code)

        self.__stack = []
        self.__blocks = []
        
        self.verbose = verbose
        
        self.__callbacks = callbacks
        
        self.inst_history = []

        if not verbose:
            self._output = io.StringIO()

        self.ops = {
                'BINARY_ADD': self.__inst_binary_add,
                'BINARY_MULTIPLY': self.__inst_binary_multiply,
                'BINARY_SUBTRACT': self.__inst_binary_subtract,
                'BINARY_MODULO': self.__inst_binary_modulo,
                'BINARY_SUBSCR': self.__inst_binary_subscr,
                'BINARY_TRUE_DIVIDE': self.__inst_binary_true_divide,
                'BINARY_FLOOR_DIVIDE': self.__inst_binary_floor_divide,
                'BINARY_POWER': self.__inst_binary_power,
                'BUILD_LIST': self.__build_list,
                'BUILD_SLICE': self.__inst_build_slice,
                'BUILD_TUPLE': self.__inst_build_tuple,
                'CALL_FUNCTION': self.call_function,
                'COMPARE_OP': self.__inst_compare_op,
                'IMPORT_NAME': self.__inst_import_name,
                'LOAD_ATTR': self.__inst_load_attr,
                'LOAD_BUILD_CLASS': self.__inst_load_build_class,
                'LOAD_CONST': self.__inst_load_const,
                'LOAD_GLOBAL': self.__inst_load_global,
                'LOAD_FAST': self.__inst_load_fast,
                'LOAD_NAME': self.__inst_load_name,
                'MAKE_FUNCTION': self.__inst_make_function,
                'POP_TOP': self.__inst_pop_top,
                'RETURN_VALUE': self.__inst_return_value,
                'STORE_NAME': self.__inst_store_name,
                'STORE_FAST': self.__inst_store_fast,
                'SETUP_LOOP': self.__inst_setup_loop,
                'GET_ITER': self.__inst_get_iter,
                'FOR_ITER': self.__inst_for_iter,
                'JUMP_ABSOLUTE': self.__inst_jump_absolute,
                'POP_BLOCK': self.__inst_pop_block,
                'POP_JUMP_IF_TRUE': self.__inst_pop_jump_if_true,
                'UNPACK_SEQUENCE': self.__inst_unpack_sequence,
                'RAISE_VARARGS': self.__inst_raise_varargs,
                'UNARY_NEGATIVE': self.__inst_unary_negative,
                'UNARY_POSITIVE': self.__inst_unary_positive,
                'YIELD_VALUE': self.__inst_yield_value,
                }
    
    def contains_op(self, opname):
        for i in self.instructions:
            if i.opname == opname:
                return True
        return False

    def contains_op_history(self, inst):
        for i in self.inst_history:
            if i.opname == inst[0]:
                if inst[1] is None:
                    return True
                elif i.arg == inst[1]:
                    return True
        return False

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

    def execute(self, globals_=None, _locals=None):
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

        if self.contains_op("YIELD_VALUE"):
            return self.iterate_instructions()
        else:
            return self.execute_instructions()

    def execute_instructions(self):

        self._print('------------- begin exec')
        
        return_value_set = False
        
        self._ii = InstructionIterator(self.instructions)

        if self.verbose:
            pprint(self._ii._tab)
        
        #for i in inst:
        for i in self._ii:
            if return_value_set:
                raise RuntimeError('RETURN_VALUE is not last opcode')

            ret = self.execute_instruction(i)

            if i.opname == "RETURN_VALUE":
                return ret
        
        self._print('------------- return')

    def iterate_instructions(self):
        self._ii = InstructionIterator(self.instructions)

        if self.verbose:
            pprint(self._ii._tab)
        
        #for i in inst:
        for i in self._ii:
            yield_value = self.execute_instruction(i)
            
            if i.opname == 'YIELD_VALUE':
                yield yield_value

    def execute_instruction(self, i):
            
        ret = None

        try:
            op = self.ops[i.opname]
        except KeyError:
            raise Exception('unhandled opcode', i.opcode, i.opname, i.arg, self.__stack)
        else:
            try:
                ret = op(self.code, i)
            except Exception as e:
                print('during machine exec {}: {}'.format(i.opname, e))
                if not self.verbose:
                    print('printing output')
                    print(self._output.getvalue())
                raise
            else:
                self.inst_history.append(i)

        self._print('{:20} {}'.format(i.opname, [(repr(s) if not str(hex(id(s))) in repr(s) else s.__class__) for s in self.__stack ]))

        return ret

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
        
        # execute the original class source code
        machine = MachineClassSource(c, self.verbose)
        l = dict()
        machine.execute(self.__globals, l)

        # construct new code for class source
        a = Assembler()
        for name, value in l.items():
            a.load_const(value)
            a.store_name(name)
        a.load_const(None)
        a.return_value()
       
        #machine = Machine(self.verbose)

        f = types.FunctionType(a.code(), self.__globals, args[1])

        args = (f, *args[1:])

        self.call_callbacks('CALL_FUNCTION', callable_, *args)
                 
        return callable_(*args)

    def call_function(self, c, i):
        """
        Implement the CALL_FUNCTION_ operation.

        .. _CALL_FUNCTION: https://docs.python.org/3/library/dis.html#opcode-CALL_FUNCTION
        """

        callable_ = self.__stack[-1-i.arg]
        
        args = tuple(self.__stack[len(self.__stack) - i.arg:])
 
        self._print('call function')
        self._print('function ', callable_)
        self._print('i.arg    ', i.arg)
        self._print('args     ', args)

        self.call_callbacks('CALL_FUNCTION', callable_, *args)
   
        if isinstance(callable_, FunctionType):
            ret = callable_(*args)

        elif callable_ is builtins.__build_class__:
            ret = self.build_class(callable_, args)

        else:
            ret = callable_(*args)
        
        self.pop(1 + i.arg)
        self.__stack.append(ret)
    
    def __build_list(self, c, i):
        self.__stack.append(list(self.pop(i.arg)))

    def __inst_pop_top(self, c, i):
        self.__stack.pop()

    def __inst_setup_loop(self, c, i):
        self.__blocks.append(i.arg)
    
    def __inst_get_iter(self, c, i):
        self.__stack.append(iter(self.__stack.pop()))

    def __inst_for_iter(self, c, i):
        TOS = self.__stack[-1]
        
        try:
            self.__stack.append(TOS.__next__())
        except StopIteration:
            self.__stack.pop()
            self._ii.jump(i.arg + i.offset + 2)

    def __inst_jump_absolute(self, c, i):
        self._ii.jump(i.arg)

    def __inst_pop_block(self, c, i):
        self.__blocks.pop()

    def __inst_pop_jump_if_true(self, c, i):
        if self.__stack.pop():
            self._ii.jump(i.arg)

    def __inst_unpack_sequence(self, c, i):
        TOS = self.__stack.pop()
        for el in reversed(TOS):
            self.__stack.append(el)

    def __inst_raise_varargs(self, c, i):
        cls = self.__stack.pop()
        args = self.pop(i.arg-1)
        raise cls(*args)

    def __inst_binary_multiply(self, c, i):
        TOS = self.__stack.pop()
        TOS1 = self.__stack.pop()
        self.__stack.append(TOS1 * TOS)


    def __inst_unary_positive(self, c, i):
                TOS = self.__stack.pop()
                self.__stack.append(+TOS)
        
    def __inst_unary_negative(self, c, i):
                TOS = self.__stack.pop()
                self.__stack.append(-TOS)
        
    def __inst_binary_power(self, c, i):
                TOS = self.__stack.pop()
                TOS1 = self.__stack.pop()
                self.__stack.append(TOS1 ** TOS)


    def __inst_binary_modulo(self, c, i):
                TOS = self.__stack.pop()
                TOS1 = self.__stack.pop()
                self.__stack.append(TOS1 % TOS)

    def __inst_binary_add(self, c, i):
                TOS = self.__stack.pop()
                TOS1 = self.__stack.pop()
                self.__stack.append(TOS1 + TOS)

    def __inst_binary_subtract(self, c, i):
                TOS = self.__stack.pop()
                TOS1 = self.__stack.pop()
                self.__stack.append(TOS1 - TOS)

    def __inst_binary_subscr(self, c, i):
                TOS = self.__stack.pop()
                TOS1 = self.__stack.pop()
                self.__stack.append(TOS1[TOS])

    def __inst_binary_floor_divide(self, c, i):
                TOS = self.__stack.pop()
                TOS1 = self.__stack.pop()
                self.__stack.append(TOS1 // TOS)

    def __inst_binary_true_divide(self, c, i):
                TOS = self.__stack.pop()
                TOS1 = self.__stack.pop()
                self.__stack.append(TOS1 / TOS)

    def __inst_load_build_class(self, c, i):
        self.__stack.append(builtins.__build_class__)

    def __inst_return_value(self, c, i):
        return self.__stack.pop()
   
    def __inst_yield_value(self, c, i):
        # documentation here
        # https://docs.python.org/3.6/library/dis.html#opcode-YIELD_VALUE
        # says that YIELD_VALUE "Pops TOS and yields it from a generator"
        # but instructions have a POP_TOP after each YIELD_VALUE which was 
        # causing "pop from empty list" error
        #return self.__stack.pop()
        return self.__stack[0]

    def __inst_store_name(self, c, i):
        name = c.co_names[i.arg]
        TOS = self.__stack.pop()
        self.store_name(name, TOS)
    
    def __inst_load_const(self, c, i):
                self.__stack.append(c.co_consts[i.arg])

    def __inst_load_name(self, c, i):
                name = c.co_names[i.arg]
                self.__stack.append(self.load_name(name))

    def __inst_build_tuple(self, c, i):
                self.__stack.append(tuple(self.pop(i.arg)))
    
    def __inst_load_attr(self, c, i): 
        name = c.co_names[i.arg]
        o = self.__stack.pop()
        self.call_callbacks('LOAD_ATTR', o, name)
        a = getattr(o, name)

        if isinstance(a, FunctionTypeClassFunction):
            a.object = o

        self.__stack.append(a)
    
    def __inst_compare_op(self, c, i):
                TOS = self.__stack.pop()
                TOS1 = self.__stack.pop()
                self.__stack.append(Machine.cmp_op(i.arg)(TOS1, TOS))

    def __inst_import_name(self, c, i):
                TOS = self.__stack.pop()
                TOS1 = self.__stack.pop()
                self.call_callbacks('IMPORT_NAME', c.co_names[i.arg], TOS, TOS1)
                self.__stack.append(__import__(c.co_names[i.arg], fromlist=TOS, level=TOS1))

    def __inst_load_global(self, c, i):
                name = c.co_names[i.arg]
                self.__stack.append(self.load_name(name))

    def __inst_load_fast(self, c, i):
                name = c.co_varnames[i.arg]
                self.__stack.append(self._locals[name])
   
    def __inst_store_fast(self, c, i): 
                TOS = self.__stack.pop()
                name = c.co_varnames[i.arg]
                self._locals[name] = TOS

    def __inst_make_function(self, c, i):
                if i.arg != 0:
                    raise RuntimeError('not yet supported')
                
                n = dis.stack_effect(i.opcode, i.arg)

                args = self.pop(-n)

                code = self.__stack.pop()
                
                m = Machine(code, self.verbose)

                # so that all instruction history is appended inst_history object of
                # root Machine
                m.inst_history = self.inst_history
                
                if isinstance(self, MachineClassSource):
                    function_type = FunctionTypeClassFunction
                else:
                    function_type = FunctionType

                f = function_type(m, code, self.__globals, args[0])
                
                # experimenting
                #f = f.wrapped

                self.__stack.append(f)

    def __inst_build_slice(self, c, i):
                TOS = self.__stack.pop()
                TOS1 = self.__stack.pop()
                if i.arg == 2:
                    self.__stack.append(slice(TOS1, TOS))
                else:
                    TOS2 = self.__stack.pop()
                    self.__stack.append(slice(TOS2, TOS1, TOS))

class MachineClassSource(Machine): pass

