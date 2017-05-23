import numpy
import unittest

import sheets

class SetScriptPreTest(unittest.TestCase):
    def test(self):
        b = sheets.Book()
    
        b.set_script_pre('import os')
        b.do_all()
    
        self.assertEqual(
                repr(b.script_pre.exec_exc),
                "ImportError(\"module 'os' is not allowed\",)")
    
        b.set_script_pre("a = 1\n")
    
        b.set_cell('0', 0, 0, "a")
        
        self.assertEqual(
                b['0'][0, 0],
                1)

