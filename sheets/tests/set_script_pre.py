import numpy
import sheets

def test():
    b = sheets.Book()

    expected_output = 'Traceback (most recent call last):\n  File "/home/crymal/git/python_packages/web_sheets/sheets/script.py", line 46, in execute\n    exec(self.code, g)\n  File "<script>", line 1, in <module>\n  File "/home/crymal/git/python_packages/web_sheets/sheets/__init__.py", line 42, in builtin___import__\n    raise ImportError("module \'{}\' is not allowed".format(name_split[0]))\nImportError: module \'os\' is not allowed\n'

    b.set_script_pre('import os')
    b.do_all()

    #print(repr(b.script_pre.output))

    if b.script_pre.output != expected_output:
        raise RuntimeError('output does not match expected')

    b.set_script_pre("import math\n")

    b.set_cell(0, 0, 0, "math.sin(math.pi)")
    
    s = b.sheets[0]

    if s.cells.cells[0,0].exception_eval is not None:
        raise RuntimeError('cell exception')

if __name__ == '__main__':
    test()

