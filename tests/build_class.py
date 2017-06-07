
import builtins

bc = builtins.__build_class__

class Foo(object):
    def func(self):
        pass

def class_func():
    def func(self):
        pass

cls = bc(class_func, 'Foo', object)

print(Foo)
print(cls)

print(Foo.func)
print(cls.func)



