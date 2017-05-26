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

class FunctionTest(unittest.TestCase):
    def test_indexof(self):
        b = sheets.Book(sheets.tests.settings.Settings)
        
        func_indexof(b)

        print('test indexof', b['0'][0, 1])









