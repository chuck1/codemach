import sys
print(sys.path)
from codemach.assembler import Assembler

def test1():
 
    asm = Assembler()
    
    asm.load_const(2)
    asm.load_const(3)
    asm.binary_add()
    asm.return_value()
    
    c = asm.code()
    
    assert eval(c) == 5

def test2():
 
    asm = Assembler()
    
    def func(*args): return args

    asm.load_name('func')
    asm.load_const(0)
    asm.load_const(1)
    asm.call_function(2)
    asm.return_value()
    
    c = asm.code()

    assert eval(c) == (0, 1)

