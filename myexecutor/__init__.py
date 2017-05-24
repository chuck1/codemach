#!/usr/bin/env python3

import sys
import dis
import types

class Executor(object):

    def __init__(self):
        self.__stack = []

        self.watch = {}

    def exec(self, code, _globals=globals()):
        
        self.__globals = _globals

        return self.exec_instructions(code)

    def emmit(self, _callable, args):
        if _callable in self.watch:
            self.watch[_callable](_callable, args)

    def load_name(self, name):
        if name in self.__globals:
            return self.__globals[name]
        
        return getattr(self.__globals['__builtins__'], name)

    def pop(self, n):
        poped = self.__stack[len(self.__stack) - n:]
        del self.__stack[len(self.__stack) - n:]
        return poped
        
    def exec_instructions(self, c, fai=None):

        inst = dis.Bytecode(c)
        
        return_value_set = False
    
        for i in inst:

            if return_value_set:
                raise RuntimeError('RETURN_VALUE is not last opcode')
    
            #print('se',dis.stack_effect(i.opcode, i.arg))
            if i.opcode == 1:
                self.__stack.pop()

            elif i.opcode == 23:
                # BINARY_ADD
                TOS = self.__stack.pop()
                TOS1 = self.__stack.pop()
                self.__stack.append(TOS + TOS1)

            elif i.opcode == 25:
                # BINARY_SUBSCR
                TOS = self.__stack.pop()
                TOS1 = self.__stack.pop()
                self.__stack.append(TOS1[TOS])

            elif i.opcode == 83:
                # RETURN_VALUE
                return_value = self.__stack.pop()
                return_value_set = True

            elif i.opcode == 90:
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
                self.__stack.append(getattr(o, name))

            elif i.opcode == 116:
                # LOAD_GLOBAL
                name = c.co_names[i.arg]
                self.__stack.append(self.load_name(name))

            elif i.opcode == 124:
                # LOAD_FAST:
                self.__stack.append(self.__stack[fai + i.arg])
    
            elif i.opcode == 131:
                # CALL_FUNCTION
                code_or_callable = self.__stack[-1-i.arg]
                
                firstargindex = len(self.__stack)-i.arg
                
                args = self.__stack[-i.arg:]
    
                if code_or_callable.__class__.__name__ == 'code':
                    ret = self.exec_instructions(code_or_callable, firstargindex)
                else:
                    self.emmit(code_or_callable, args)
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
                raise RuntimeError('unhandled opcode',i.opcode,i.opname,self.__stack)
    
            print('%13s' % i.opname, self.__stack)
    
        return return_value
            

if __name__ == '__main__':
    e = Executor()

    s = """def func(a, b):\n  return a + b\nfunc(2, 3)"""
    s = """object.__getattribute__(object, '__class__')"""

    c = compile(s, '<string>', 'eval')

    print(e.exec(c))









