import numpy
import sheets

def test():
    b = sheets.Book()

    b.set_script_pre('import os')
    b.do_all()

    assert(repr(b.script_pre.exec_exc) == "ImportError(\"module 'os' is not allowed\",)")

    b.set_script_pre("import math\n")

    b.set_cell(0, 0, 0, "math.sin(math.pi)")
    
    s = b.sheets[0]

    if s.cells.cells[0,0].exception_eval is not None:
        raise RuntimeError('cell exception')

if __name__ == '__main__':
    test()

