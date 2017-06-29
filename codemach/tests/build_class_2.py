import builtins
import dis
import types

s = """
class Foo(object):
    a = 1
    def func(self):
        pass
    locals()['b'] = 2
"""

c1 = compile(s, '<string>', 'exec')
c2 = c1.co_consts[0]

dis.dis(c2)

def wrap(f):
    def wrapper(*args):
        #return f(*args)
        c = f.__code__
        #l = dict()
        exec(c, globals(), locals())
        print(locals())
    return wrapper

f1 = types.FunctionType(c2, globals())

f2 = wrap(f1)

dis.dis(f2.__code__)


bc = builtins.__build_class__

cls1 = bc(f1, 'Foo', object)
cls2 = bc(f2, 'Foo', object)


print(cls1.__dict__)
print(cls2.__dict__)


