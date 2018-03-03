import dis
from codemach.machine import Machine

def analyze_code(c):
    print('consts')
    for const in c.co_consts:
        print(f'\t{const!r}')
    print('flags   ',c.co_flags)
    print('cellvars', c.co_cellvars)
    print('dis')
    dis.dis(c)

s = "class Foo:\n def func(self, a): pass\na=Foo()"

c = compile(s, "", "exec")

m = Machine(c)

m.execute()

print('global')
analyze_code(c)

c1 = c.co_consts[0]

print('class')
analyze_code(c1)

c2 = c1.co_consts[1]

print('func')
analyze_code(c2)

