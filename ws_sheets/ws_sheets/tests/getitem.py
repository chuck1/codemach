
class Foo(object):
    def __getitem__(self, args):
        print(repr(args))

    def func(self, args):
        print(repr(args))


f = Foo()

f[0]
f[(0,)]
f[0,0]
f[(0,0)]

