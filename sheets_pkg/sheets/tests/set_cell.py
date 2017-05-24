import numpy
import unittest

import sheets

import sheets.tests.settings

class SetCellTest(unittest.TestCase):
    def test(self):
        b = sheets.Book(sheets.tests.settings.Settings)
    
        b['0'][0, 0] = '2+2'
        self.assertEqual(b['0'][0, 0], 4)

        b['0'][0, 0] = '4'
        b['0'][0, 1] = 'sheet[0, 0]'
        self.assertEqual(b['0'][0, 1], 4)

        b['0'][0, 0] = '2'
        b['0'][0, 1] = '3'
        b['0'][0, 2] = 'sheet[0, 0:2]'
        print('cell 0,0 = ', b['0'][0, 0])
        print('cell 0,1 = ', b['0'][0, 1])
        print('cell 0,2 = ', b['0'][0, 2])
        self.assertEqual(numpy.all(b['0'][0, 2] == numpy.array([2, 3])), True)

        b['0'][0, 0] = 'sheet[0, 0]'
        self.assertEqual(repr(b['0'][0, 0].item()), "RuntimeError('recursion',)")

        b['0'][0, 0] = ''
        self.assertEqual(b['0'][0, 0].item(), None)
    
        b['0'][0, 0] = '4'
        b['1'][0, 0] = 'book[\'0\'][0, 0]'
        self.assertEqual(b['1'][0, 0], 4)
    
        
    
