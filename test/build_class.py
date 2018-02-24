from codemach.machine import Machine

s = """
class Foo:
    def func(self, a):
        pass
a=Foo()
"""

c = compile(s, "", "exec")

m = Machine(c)

m.execute()

