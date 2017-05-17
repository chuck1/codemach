
import sheets

import unittest

def code_analysis(code):
    print(code)
    for name in code.co_names:
        print('  '+name)
        if name[:2] == '__':
            print('    not allowed')


class SecurityTest(unittest.TestCase):

    def test_helper(self):
        b = sheets.Book()
        
        s = b.sheets['0']
        
        b.set_cell('0', 0, 1, "1")
        
        ########

        b.set_cell('0', 0, 0, "cellshelper.__getitem__.__globals__['__builtins__']['open']")

        c = s.cells.cells[0, 0]

        print('cell =', c)
        
        print(s.cells.cells[0, 0].value)

        if c.code is not None:
            code_analysis(c.code)

        ########

        b.set_cell('0', 0, 0, "getattr(cellshelper, '__getitem__')")

        c = s.cells.cells[0, 0]

        print('cell =', c)
        
        print(s.cells.cells[0, 0].value)

        if c.code is not None:
            code_analysis(c.code)

        ########

        b.set_cell('0', 0, 0, "cellshelper[0,1]")

        c = s.cells.cells[0, 0]

        print('cell =', c)
        print(c.code.co_names)
        
        print(s.cells.cells[0, 0].value)



