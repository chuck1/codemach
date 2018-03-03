
class Foo: pass

def func(*args):
    print('func', args)

Foo.func = func


print(Foo.func)

foo = Foo()

print(foo.func)



