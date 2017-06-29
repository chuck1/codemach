from codemach import Assembler

def test1():
 
    asm = Assembler()
    
    asm.load_const(2)
    asm.load_const(3)
    asm.binary_add()
    asm.return_value()
    
    #print_asm(insts.insts)
    
    c = asm.code()
    
    print(c)
    
    print('eval')
    print(eval(c))
 
