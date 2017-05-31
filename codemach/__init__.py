#!/usr/bin/env python3

import sys
import dis
import types
import operator

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
        self._locals = {}
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

    def exec(self, code, _globals=globals()):
        
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

    def pop(self, n):
        poped = self.__stack[len(self.__stack) - n:]
        del self.__stack[len(self.__stack) - n:]
        return poped
        
    def exec_instructions(self, c):

        if self.verbose > 0:print('------------- begin exec')

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

            elif i.opcode == 83:
                # RETURN_VALUE
                return_value = self.__stack.pop()
                return_value_set = True

            elif i.opcode == 90:
                # STORE_NAME
                self.__globals[c.co_names[i.arg]] = self.__stack.pop()

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
                code_or_callable = self.__stack[-1-i.arg]
                
                args = tuple(self.__stack[len(self.__stack) - i.arg:])
    
                if isinstance(code_or_callable, types.CodeType):
                    _c = code_or_callable
                    e = Machine(self.verbose)
                    
                    e._locals = dict((name, arg) for name, arg in zip(
                        _c.co_varnames[:_c.co_argcount], args))
                    
                    ret = e.exec(_c, self.__globals)
                else:
                    self.signal['CALL_FUNCTION'].emmit(code_or_callable, *args)

                    ret = code_or_callable(*args)
                
                self.pop(1 + i.arg)
                self.__stack.append(ret)

            elif i.opcode == 132:
                # MAKE_FUNCTION
                if i.arg != 0:
                    raise RuntimeError('not yet supported')
                
                #print(i.opname, i.opcode, i.arg, dis.stack_effect(i.opcode, i.arg))
                n = dis.stack_effect(i.opcode, i.arg)
                self.pop(-n)

                code = self.__stack.pop()
                self.__stack.append(code)

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
        


