
import sheets

import unittest

class SecurityTest(unittest.TestCase):

    def test_helper(self):
        b = sheets.Book()
        
        s = b.sheets['0']
        
        b.set_cell('0', 0, 1, "1")

        b.set_cell('0', 0, 0, "cellshelper.__getitem__.__globals__['__builtins__']['open']")

        c = s.cells.cells[0, 0]

        print('cell =', c)
        
        print(s.cells.cells[0, 0].value)


        if c.code is not None:
            print(c.code.co_names)
            for name in c.code.co_names:
                if name[:2] == '__':
                    print('not allowed')



        b.set_cell('0', 0, 0, "cellshelper[0,1]")

        c = s.cells.cells[0, 0]

        print('cell =', c)
        print(c.code.co_names)
        
        print(s.cells.cells[0, 0].value)



