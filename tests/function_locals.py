import dis
import builtins
import types

def func():
    def f(): pass

s = """
def f():pass
"""

def wrap(f):
    def wrapper():
        return f()
    return wrapper

bc = builtins.__build_class__


def test(c):
    g = globals()
    l = {}

    exec(c, g, l)

    print()
    dis.dis(c)
    print()

    print('locals:', l.keys())

    cls = bc(types.FunctionType(c, globals()), 'Foo', object)

    print(cls)
    print(dir(cls))


cls = bc(func, 'Foo', object)

print(cls)

c = compile(s, '<string>', 'exec')

print('func.__code__ ----------------------')
test(func.__code__)

print('c ----------------------')
test(c)



