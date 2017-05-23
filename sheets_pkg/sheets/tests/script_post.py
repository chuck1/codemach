import numpy
import unittest

import sheets

class ScriptPostTest(unittest.TestCase):
    def test(self):
        b = sheets.Book()
    
        b.set_script_pre('import math\na=math.pi')

        b['0'][0, 0] = 'a'

        b.set_script_post("print(book['0'][0, 0])")

        b.do_all()
   
        print(repr(b.script_post.output))

        self.assertEqual(b.script_post.output, '3.141592653589793\n')


