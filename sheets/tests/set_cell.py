import numpy
import sheets

def test():
    s = sheets.Sheet()

    print(numpy.shape(s.cells))

    s.set_cell(0,0,'2+2')

    print(numpy.shape(s.cells))

    print(s.cells[0,0].value)

if __name__ == '__main__':
    test()

