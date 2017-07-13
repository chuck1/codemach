import dis
import types

__all__ = ['Assembler']

def inst_to_bytes(inst):
    return bytes([
        inst.opcode,
        inst.arg])

class Assembler(object):
    def __init__(self):
        self.offset = 0
        self.insts = list()
        self.consts = list()
        self.names = list()
        self.varnames = list()

    def get_const_arg(self, v):
        if v not in self.consts:
            self.consts.append(v)
        return self.consts.index(v)

    def get_name_arg(self, v):
        if v not in self.names:
            self.names.append(v)
        return self.names.index(v)

    def load_const(self, argval):
        inst = dis.Instruction(
                'LOAD_CONST',
                dis.opname.index('LOAD_CONST'),
                self.get_const_arg(argval),
                argval,
                repr(argval),
                self.offset,
                None,
                False)
        
        self.offset += 2
        
        self.insts.append(inst)

    def load_name(self, argval):
        inst = dis.Instruction(
                'LOAD_NAME',
                dis.opname.index('LOAD_NAME'),
                self.get_name_arg(argval),
                argval,
                repr(argval),
                self.offset,
                None,
                False)
        
        self.offset += 2
        
        self.insts.append(inst)

    def store_name(self, argval):
        inst = dis.Instruction(
                'STORE_NAME',
                dis.opname.index('STORE_NAME'),
                self.get_name_arg(argval),
                argval,
                repr(argval),
                self.offset,
                None,
                False)
        
        self.offset += 2
        
        self.insts.append(inst)

    def binary_add(self):
        inst = dis.Instruction(
                'BINARY_ADD',
                dis.opname.index('BINARY_ADD'),
                0,
                None,
                '',
                self.offset,
                None,
                False)
        
        self.offset += 1
        
        self.insts.append(inst)

    def return_value(self):
        inst = dis.Instruction(
                'RETURN_VALUE',
                dis.opname.index('RETURN_VALUE'),
                0,
                None,
                '',
                self.offset,
                None,
                False)
        
        self.offset += 2
        
        self.insts.append(inst)

    def call_function(self, argc):
        inst = dis.Instruction(
                'CALL_FUNCTION',
                dis.opname.index('CALL_FUNCTION'),
                argc,
                argc,
                repr(argc),
                self.offset,
                None,
                False)
        
        self.offset += 2
        
        self.insts.append(inst)

    def code(self):
    
        b = b''.join(bytes([i.opcode, i.arg]) for i in self.insts)

        c = types.CodeType(
                0,
                0,
                0,
                2,
                64,
                b,
                tuple(self.consts),
                tuple(self.names),
                tuple(self.varnames),
                '<constructed code>',
                '<module>',
                0,
                b'')

        return c


 
   

