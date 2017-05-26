import numpy
import unittest

import sheets.tests.settings

def func_import(bp):

    bp.set_script_pre('import math\nprint(math)\n')

    bp.set_cell('0', 0, 0, 'math.pi')

string_named_range = """
def a():
    return book['0'][0:2, 0]
"""

def func_named_range(bp):

    bp.set_script_pre(string_named_range)

    bp.set_cell('0', 0, 0, '1')
    bp.set_cell('0', 1, 0, '2')
    bp.set_cell('0', 2, 0, 'a()')

def func_sum(bp):

    bp.set_cell('0', 0, 0, '1')
    bp.set_cell('0', 1, 0, '2')
    bp.set_cell('0', 2, 0, '3')
    bp.set_cell('0', 3, 0, '4')
    bp.set_cell('0', 4, 0, '5')

    bp.set_cell('0', 0, 1, 'sum(sheet[0:5, 0])')

string_indexof = """
import numpy
def indexof(arr, a):
    i = numpy.argwhere(arr == a)
    return i
"""

def func_indexof(bp):

    bp.set_script_pre(string_indexof)

    bp.set_cell('0', 0, 0, '1')
    bp.set_cell('0', 1, 0, '2')
    bp.set_cell('0', 2, 0, '3')
    bp.set_cell('0', 3, 0, '4')
    bp.set_cell('0', 4, 0, '5')

    bp.set_cell('0', 0, 1, 'indexof(sheet[0:5, 0], 3)')

string_lookup = """
import numpy
def lookup(a, b, c):
    return c[numpy.argwhere(b == a)]
"""

def func_lookup(b):

    b.set_script_pre(string_lookup)

    b.set_cell('0', 0, 0, "'Bob'")
    b.set_cell('0', 1, 0, "'Sue'")
    b.set_cell('0', 2, 0, "'Jim'")
    b.set_cell('0', 3, 0, "'Pat'")
    
    b.set_cell('0', 0, 1, "'apple'")
    b.set_cell('0', 1, 1, "'banana'")
    b.set_cell('0', 2, 1, "'pear'")
    b.set_cell('0', 3, 1, "'fig'")

    b.set_cell('0', 0, 2, """lookup('Sue', sheet[:, 0], sheet[:, 1])""")

class FunctionTest(unittest.TestCase):
    def test_indexof(self):
        b = sheets.Book(sheets.tests.settings.Settings)
        
        func_indexof(b)

        print('test indexof', b['0'][0, 1])
        print('test indexof', b['0'].cells.cells[0, 1])
        print('test indexof', repr(b['0'].cells.cells[0, 1].value))

    def test_lookup(self):
        b = sheets.Book(sheets.tests.settings.Settings)
        
        func_lookup(b)

        print('test lookup', b['0'][0, 2])
        print('test lookup', b['0'].cells.cells[0, 2])
        print('test lookup', repr(b['0'].cells.cells[0, 2].value))

        self.assertEqual(
                numpy.array([['banana']]),
                b['0'][0, 2])







