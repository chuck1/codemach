
def insp(f):
    print()
    for d in dir(f):
        print(d, getattr(f, d))

class Foo(object):
    a = 1
    def func(self):
        pass

    def func2(self):

        def func3():
            self.a += 1
            return self.a

        return func3

f = Foo()

insp(f.func)

def gfunc():
    f.a += 1
    return f.a

insp(gfunc)

insp(f.func2())

