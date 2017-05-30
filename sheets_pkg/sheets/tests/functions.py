import numpy
import unittest

import sheets.tests.settings

string_named_range = """
def a():
    return book['0'][0:2, 0]
"""

string_indexof = """
import numpy
def indexof(arr, a):
    i = numpy.argwhere(arr == a)
    return i
"""

string_lookup = """
import numpy
def lookup(a, b, c):
    return c[numpy.argwhere(b == a)]
"""

string_datetime = """
import datetime
import pytz
"""

string_strings = """
s = "The quick brown fox jumps over the lazy dog"
"""


class TestImport(unittest.TestCase):
    def setup(self, bp):
    
        bp.set_script_pre('import math\nprint(math)\n')
    
        bp.set_cell('0', 0, 0, 'math.pi')
    
class TestNamedRange(unittest.TestCase):
    def setup(self, bp):
    
        bp.set_script_pre(string_named_range)
    
        bp.set_cell('0', 0, 0, '1')
        bp.set_cell('0', 1, 0, '2')
        bp.set_cell('0', 2, 0, 'a()')
    
class TestSum(unittest.TestCase):
    def setup(self, bp):
    
        bp.set_cell('0', 0, 0, '1')
        bp.set_cell('0', 1, 0, '2')
        bp.set_cell('0', 2, 0, '3')
        bp.set_cell('0', 3, 0, '4')
        bp.set_cell('0', 4, 0, '5')
    
        bp.set_cell('0', 0, 1, 'sum(sheet[0:5, 0])')
    
class TestIndexof(unittest.TestCase):
    def setup(self, bp):
    
        bp.set_script_pre(string_indexof)
    
        bp.set_cell('0', 0, 0, '1')
        bp.set_cell('0', 1, 0, '2')
        bp.set_cell('0', 2, 0, '3')
        bp.set_cell('0', 3, 0, '4')
        bp.set_cell('0', 4, 0, '5')
    
        bp.set_cell('0', 0, 1, 'indexof(sheet[0:5, 0], 3)')

    def test(self):
        b = sheets.Book(sheets.tests.settings.Settings)
        self.setup(b)

        print('test indexof', b['0'][0, 1])
        print('test indexof', b['0'].cells.cells[0, 1])
        print('test indexof', repr(b['0'].cells.cells[0, 1].value))
    
class TestLookup(unittest.TestCase):
    def setup(self, b):
    
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
    
    def test(self):
        b = sheets.Book(sheets.tests.settings.Settings)
        self.setup(b)

        print('test lookup', b['0'][0, 2])
        print('test lookup', b['0'].cells.cells[0, 2])
        print('test lookup', repr(b['0'].cells.cells[0, 2].value))

        self.assertEqual(
                numpy.array([['banana']]),
                b['0'][0, 2])

class TestDatetime(unittest.TestCase):
    def setup(self, b):
        b.set_script_pre(string_datetime)
    
        b.set_cell('0', 0, 0, "datetime.datetime.now()")
        b.set_cell('0', 0, 1, "sheet[0, 0].item().tzinfo")
        b.set_cell('0', 1, 0, "datetime.datetime.utcnow()")
        b.set_cell('0', 1, 1, "sheet[1, 0].item().tzinfo")
        b.set_cell('0', 2, 0, "datetime.datetime.now(pytz.utc)")
        b.set_cell('0', 2, 1, "sheet[2, 0].item().tzinfo")

    def test(self):
        b = sheets.Book(sheets.tests.settings.Settings)
        self.setup(b)

        print('test datetime', b['0'][0, 0])
        print('test datetime', b['0'][0, 1])
        print('test datetime', b['0'][1, 0])
        print('test datetime', b['0'][1, 1])
        print('test datetime', b['0'][2, 0])
        print('test datetime', b['0'][2, 1])

class TestStrings(unittest.TestCase):
    def setup(self, b):
        b.set_docs("""
`python str documentation`_

.. _`python str documentation`: https://docs.python.org/3.6/library/stdtypes.html#text-sequence-type-str
""")

        b.set_script_pre(string_strings)

        b.set_cell('0', 0, 0, "s.lower()")
        b.set_cell('0', 1, 0, "s.upper()")
        b.set_cell('0', 2, 0, "s[16:19]")
    
    
    def test(self):
        b = sheets.Book(sheets.tests.settings.Settings)
        self.setup(b)

class TestMath(unittest.TestCase):
    def setup(self, b):
        b.set_docs("""
`python standard library: math`__

.. _math: https://docs.python.org/3/library/math.html

__ math_
""")

        b.set_script_pre("""
import math
""")

        b.set_cell('0', 0, 0, "math.pi")
        b.set_cell('0', 1, 0, "math.sin(math.pi)")
        b.set_cell('0', 2, 0, "math.cos(math.pi)")
        b.set_cell('0', 3, 0, "math.sqrt(4)")
        b.set_cell('0', 4, 0, "math.pow(2, 2)")
        b.set_cell('0', 5, 0, "math.exp(1)")

class TestNumericalTypes(unittest.TestCase):
    def setup(self, b):
        b.set_docs("""
`python numerical types`__

.. _link: https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex

__ link_
""")

        b.set_script_pre("""
x = 3
y = 2
""")

        b.set_cell('0',  0, 0, "x + y")
        b.set_cell('0',  1, 0, "x - y")
        b.set_cell('0',  2, 0, "x / y")
        b.set_cell('0',  3, 0, "x // y")
        b.set_cell('0',  4, 0, "x % y")
        b.set_cell('0',  5, 0, "-x")
        b.set_cell('0',  6, 0, "+x")
        b.set_cell('0',  7, 0, "abs(x)")
        b.set_cell('0',  8, 0, "int(x)")
        b.set_cell('0',  9, 0, "float(x)")
        b.set_cell('0', 10, 0, "complex(x, y)")
        b.set_cell('0', 11, 0, "complex(x, y).conjugate()")
        b.set_cell('0', 12, 0, "divmod(x, y)")
        b.set_cell('0', 13, 0, "pow(x, y)")
        b.set_cell('0', 14, 0, "x ** y")
    
    def test(self):
        b = sheets.Book(sheets.tests.settings.Settings)
        self.setup(b)
        





