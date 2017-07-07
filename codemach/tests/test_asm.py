from codemach import Assembler

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
    
    asm.load_name('list')
    
    c = asm.code()
    

