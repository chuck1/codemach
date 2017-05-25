import numpy
import unittest

import sheets
import sheets.tests.settings

class ScriptPreSecurityTest(unittest.TestCase):
    def test(self):
        b = sheets.Book(sheets.tests.settings.Settings)
    
        b.set_script_pre('book.do_all')
        
        b.do_all()
        
        print('output')
        print(repr(b.script_pre.output))
        print('exc')
        print(repr(b.script_pre.exec_exc))
        print(repr(b.script_pre.exec_exc.__class__))
        
        """
        self.assertEqual(
                repr(),
                "ImportError(\"module 'os' is not allowed\",)")
        """

