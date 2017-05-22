import numpy
import unittest

import sheets

class CellSetter(object):
    def __init__(self, sk, r, c, string):
        self.sk = sk
        self.r = r
        self.c = c
        self.string = string

    def __call__(self, sheet):
        sheet = book.sheets[self.sk]
        sheet.set_cell(self.r, self.c, self.string)

class CellChecker(object):
    def __init__(self, sk, r, c, value):
        self.sk = sk
        self.r = r
        self.c = c
        self.value = value

    def __call__(self, test, book):
        sheet = book.sheets[self.sk]
        test.assertEqual(sheet.cells.cells[self.r, self.c].value, self.value)

class CellArrayChecker(object):
    def __init__(self, sk, r, c, value):
        self.sk = sk
        self.r = r
        self.c = c
        self.value = value

    def __call__(self, test, book):
        a = book.sheets[self sk].cells.cells[self.r, self.c].value
        b = self.value
        print(a, b, a==b)
        test.assertEqual(numpy.all(a == b), True)

simple_set_cell_tests = [
        (
            [
                CellSetter('0', 0, 0, '2+2'),],
            [
                CellChecker('0', 0, 0, 4)]),
        (
            [
                CellSetter('0', 0, 0, 'book'),],
            [
                ]),
        (
            [
                CellSetter('0', 0, 0, 'book.test_func()'),],
            [
                ]),
        (
            [
                CellSetter('0', 0, 0, '4'),
                CellSetter('0', 0, 1, 'SheetHelper()[0,0]'),],
            [
                CellChecker('0', 0, 1, 4)]),
        (
            [
                CellSetter('0', 0, 0, '2'),
                CellSetter('0', 0, 1, '3'),
                CellSetter('0', 0, 2, 'sheet[0, 0:2]'),
                ],
            [
                CellArrayChecker(0, 2, numpy.array([2, 3]))]),
        ]

class SetCellTest(unittest.TestCase):
    def test(self):
        b = sheets.Book()
    
        s = b.sheets["0"]
        
        for setters, checkers in simple_set_cell_tests:
            for setter in setters:
                print("[{},{}] = {}".format(setter.r, setter.c, setter.string))
                setter(s)
                print(s.cells.cells[setter.r, setter.c].value)
            for checker in checkers:
                print("[{},{}] -> {}".format(checker.r, checker.c, repr(checker.value)))
                checker(self, s)

        return
        b.sheets['0'].set_cell(0, 0, '2+2')
            [
                CellChecker('0', 0, 0, 4)]),
        (
            [
                CellSetter('0', 0, 0, 'book'),],
            [
                ]),
        (
            [
                CellSetter('0', 0, 0, 'book.test_func()'),],
            [
                ]),
        (
            [
                CellSetter('0', 0, 0, '4'),
                CellSetter('0', 0, 1, 'SheetHelper()[0,0]'),],
            [
                CellChecker('0', 0, 1, 4)]),
        (
            [
                CellSetter('0', 0, 0, '2'),
                CellSetter('0', 0, 1, '3'),
                CellSetter('0', 0, 2, 'sheet[0, 0:2]'),
                ],
            [
                CellArrayChecker(0, 2, numpy.array([2, 3]))]),
    
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
        
    
