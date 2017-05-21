import numpy
import unittest

import sheets

class CellSetter(object):
    def __init__(self, r, c, string):
        self.r = r
        self.c = c
        self.string = string

    def __call__(self, sheet):
        sheet.set_cell(self.r, self.c, self.string)

class CellChecker(object):
    def __init__(self, r, c, value):
        self.r = r
        self.c = c
        self.value = value

    def __call__(self, sheet):
        return (sheet.cells.cells[self.r, self.c].value, self.value)

simple_set_cell_tests = [
        (
            [
                CellSetter(0, 0, '2+2'),],
            [
                CellChecker(0, 0, 4)]),
        (
            [
                CellSetter(0, 0, '2+2'),
                CellSetter(0, 1, 'SheetHelper()[0,0]'),],
            [
                CellChecker(0, 1, 4)]),
        ]

class SetCellTest(unittest.TestCase):
    def test(self):
        b = sheets.Book()
    
        s = b.sheets["0"]
        
        for setters, checkers in simple_set_cell_tests:
            for setter in setters:
                print("[{},{}] = {}".format(setter.r, setter.c, setter.string))
                setter(s)
            for checker in checkers:
                print("[{},{}] -> {}".format(checker.r, checker.c, repr(checker.value)))
                self.assertEqual(*checker(s))

        return
        b.set_cell("0", 0, 2, "cellshelper[0,0:1]")
        
        assert(numpy.all(s.cells.cells[0, 2].value == numpy.array([4, 4])))
    
        b.set_cell("0", 1, 0, "cellshelper[1, 0]")
        
        #print("cell val:", repr(s.cells.cells[1, 0].value))
        #print("cell exc:", repr(s.cells.cells[1, 0].exception_eval))
        
        assert(repr(s.cells.cells[1, 0].value) == "RuntimeError('recursion',)")
    
        b.set_cell("0", 1, 0, "cellshelper[1, 1]")
    
        #print(repr(s.cells.cells[1, 0].value))
        assert(s.cells.cells[1, 0].value.item() is None)
    
        b.set_cell("0", 1, 1, "2+2")
    
        print(repr(s.cells.cells[1, 1].value))
        print(repr(s.cells.cells[1, 0].value))
        assert(s.cells.cells[1, 0].value.item() == 4)
    
        b.set_cell("0", 0, 0, "[0, 1]")
        print(s.cells.cells[0, 0].value)
        b.set_cell("0", 0, 0, "(0, 1)")
        print(s.cells.cells[0, 0].value)
        b.set_cell("0", 0, 0, "{'a':0, 'b':1}")
        print(s.cells.cells[0, 0].value)
        b.set_cell("0", 0, 0, "{0, 1}")
        print(s.cells.cells[0, 0].value)
    
        b.set_cell("0", 0, 0, "cellshelper[0, 0, \"1\"]")
        print(s.cells.cells[0, 0].value)
    
        b.set_cell("1", 0, 0, "\"I am a cell in sheet \\\"1\\\"\"")
    
        b.set_cell("0", 0, 0, "cellshelper[0, 0, \"1\"]")
        print(s.cells.cells[0, 0].value)
        
    
