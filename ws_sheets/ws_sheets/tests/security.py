
import sheets

import unittest

import sheets.tests.settings

def code_analysis(code):
    print(code)
    #print(dir(code))
    print('co_consts')
    for name in code.co_consts:
        print('  '+name)
    print('co_names')
    for name in code.co_names:
        print('  '+name)
        if name[:2] == '__':
            print('    not allowed')

class SecurityTest(unittest.TestCase):

    def test(self):
        b = sheets.Book(sheets.tests.settings.Settings)
        s = b['0']

        ########
        print()

        b['0'][0, 0] = "dir(book)"

        c = s.cells.cells[0, 0]

        print('cell =', c)
        print(repr(c.value))

        ########
        print()

        b['0'][0, 0] = "dir(book.__eq__)"

        c = s.cells.cells[0, 0]

        #print(repr(b['0'][0, 0]))
        print('cell =', c)
        print(repr(c.value))
        return
        
        self.assertEqual(
                repr(b['0'][0, 0].item()),
                'NotAllowedError("cell not allowed to access \'__eq__\'",)')


        ########
        print()

        b['0'][0, 0] = "book.test_func.__func__"

        c = s.cells.cells[0, 0]

        print('cell =', c)
        print(repr(c.value))

        ########
        print()

        b['0'][0, 0] = "book.test_func()"

        c = s.cells.cells[0, 0]

        print('cell =', c)
        print(repr(c.value))

        ########
        print()

        b['0'][0, 0] = "book.test_callable('hello','world')"

        c = s.cells.cells[0, 0]

        print('cell =', c)
        print(repr(c.value))

        ########
        print()

        b['0'][0, 0] = "book.test_callable.__call__.__func__"

        c = s.cells.cells[0, 0]

        print('cell =', c)
        print(repr(c.value))

        if c.code is not None:
            code_analysis(c.code)

        return



        ########
        print()

        b.set_cell('0', 0, 0, "getattr(getattr(cellshelper, '__getitem__'), '__globals__').keys()")

        c = s.cells.cells[0, 0]

        print('cell =', c)
        
        print(s.cells.cells[0, 0].value)

        if c.code is not None:
            code_analysis(c.code)

        ########
        print()

        b.set_cell('0', 0, 0, "dir(cellshelper)")

        c = s.cells.cells[0, 0]

        print('cell =', c)
        
        print(s.cells.cells[0, 0].value)

        if c.code is not None:
            code_analysis(c.code)

        ########
        print()

        b.set_cell('0', 0, 0, "cellshelper._CellsHelper__book")

        c = s.cells.cells[0, 0]

        print('cell =', c)
        
        print(s.cells.cells[0, 0].value)

        if c.code is not None:
            code_analysis(c.code)

        ########
        print()

        b.set_cell('0', 0, 0, "cellshelper[0,1]")

        c = s.cells.cells[0, 0]

        print('cell =', c)
        print(c.code.co_names)
        
        print(s.cells.cells[0, 0].value)



