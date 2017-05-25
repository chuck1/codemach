import numpy
import unittest

import sheets
import sheets.exception
import sheets.tests.settings

class SetScriptPreTest(unittest.TestCase):
    def test(self):
        b = sheets.Book(sheets.tests.settings.Settings)
    
        b.set_script_pre('import os')
        b.do_all()
        
        #print('output')
        #print(b.script_pre.output)

        self.assertTrue(isinstance(
                b.script_pre.exec_exc,
                sheets.exception.NotAllowedError))
    
        b.set_script_pre("a = 1\n")
    
        b.set_cell('0', 0, 0, "a")
        
        self.assertEqual(
                b['0'][0, 0],
                1)

