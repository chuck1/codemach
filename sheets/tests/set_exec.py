import numpy
import sheets

def test():
    s = sheets.Sheet()

    print(s.get_globals())

    s.set_exec('import math\nfrom math import sin\npie = math.pi')
    
    print(s.get_globals())

    try:
        s.set_exec('import matplotlib.pyplot')
    except ImportError as e:
        pass
    else:
        raise RuntimeError('test failed')
 
    print(s.get_globals())

    print(s.exec_exception_exec)
    
    s.set_cell(0,0,'sin(pie)')

    print(s.cells[0,0].value)

if __name__ == '__main__':
    test()

