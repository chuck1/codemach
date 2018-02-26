class A:
    def __init__(self):
        self.a = 1
    def f(self):
        return self.a
a1 = A()
a2 = A()

assert (a1.f is not a2.f)

