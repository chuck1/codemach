from pprint import pprint

class Foo:
    def func(self, a, b=1):
        pass

print(Foo.func.__code__.co_varnames)
print(Foo.func.__code__.co_argcount)

pprint(dir(Foo.func))

print(Foo.func.__closure__)

