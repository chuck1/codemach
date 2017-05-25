import numpy
import unittest

import sheets
import sheets.exception
import sheets.tests.settings

class ScriptPreSecurityTest(unittest.TestCase):
    def test_1(self):
        b = sheets.Book(sheets.tests.settings.Settings)
    
        b.set_script_pre('book.do_all')
        
        b.do_all()
        
        print('output')
        print(b.script_pre.output)
        print('exc')
        print(repr(b.script_pre.exec_exc))
        print(repr(b.script_pre.exec_exc.__class__))
        
        self.assertTrue(isinstance(b.script_pre.exec_exc,
            sheets.exception.NotAllowedError))
        

        b.set_script_pre('getattr(book,\'do_all\')')
        
        b.do_all()
        
        print('output')
        print(b.script_pre.output)
        print('exc')
        print(repr(b.script_pre.exec_exc))
        print(repr(b.script_pre.exec_exc.__class__))
        
        self.assertTrue(isinstance(b.script_pre.exec_exc,
            sheets.exception.NotAllowedError))
        
        
        b.set_script_pre('object.__getattribute__(book,\'do_all\')')

        b.do_all()
        
        print('output')
        print(b.script_pre.output)
        print('exc')
        print(repr(b.script_pre.exec_exc))
        print(repr(b.script_pre.exec_exc.__class__))
        
        self.assertTrue(isinstance(b.script_pre.exec_exc,
            sheets.exception.NotAllowedError))
        
        


