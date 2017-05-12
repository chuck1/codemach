import numpy
import sheets

def test():
    s = sheets.Sheet()

    expected_output = 'Traceback (most recent call last):\n  File "/home/crymal/git/python_packages/web_sheets/sheets/script.py", line 46, in execute\n    exec(self.code, g)\n  File "<script>", line 1, in <module>\n  File "/home/crymal/git/python_packages/web_sheets/sheets/__init__.py", line 45, in builtin___import__\n    raise ImportError("module \'{}\' is not allowed".format(name_split[0]))\nImportError: module \'os\' is not allowed\n'

    s.set_script_pre('import os')
    s.do_all()
    
    if s.script_pre.output != expected_output:
        raise RuntimeError('output does not match expected')

    s.set_script_pre("import math\n")

    s.set_cell(0, 0, "math.sin(math.pi)")

    if s.cells.cells[0,0].exception_eval is not None:
        raise RuntimeError('cell exception')

if __name__ == '__main__':
    test()

