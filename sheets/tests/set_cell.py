import numpy
import sheets

def test():
    s = sheets.Sheet()

    s.set_cell(0, 0, "2+2")

    assert(s.cells.cells[0, 0].value == 4)

    s.set_cell(0, 1, "cellshelper[0,0]")

    assert(s.cells.cells[0, 1].value == 4)
    
    s.set_cell(0, 2, "cellshelper[0,0:1]")
    
    assert(numpy.all(s.cells.cells[0, 2].value == numpy.array([4, 4])))

    s.set_cell(1, 0, "cellshelper[1, 0]")
    
    #print("cell val:", repr(s.cells.cells[1, 0].value))
    #print("cell exc:", repr(s.cells.cells[1, 0].exception_eval))
    
    assert(repr(s.cells.cells[1, 0].value) == "RuntimeError('recursion',)")

    s.set_cell(1, 0, "cellshelper[1, 1]")

    #print(repr(s.cells.cells[1, 0].value))
    assert(s.cells.cells[1, 0].value.item() is None)

    s.set_cell(1, 1, "2+2")

    #print(s.cells.cells[1, 0].value)
    assert(s.cells.cells[1, 0].value.item() == 4)

    print(repr(s.cells.cells[1, 0]))
    

if __name__ == '__main__':
    test()

