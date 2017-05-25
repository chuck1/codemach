
def func_import(bp):

    bp.set_script_pre('import math\nprint(math)\n')

    bp.set_cell('0', 0, 0, 'math.pi')

string_named_range = """
def a():
    return book['0'][0:1, 0]
"""

def func_named_range(bp):

    bp.set_script_pre(string_named_range)

    bp.set_cell('0', 0, 0, '1')
    bp.set_cell('0', 1, 0, '2')
    bp.set_cell('0', 2, 0, 'a()')

def get_func(s):
    
    return {
            'import': func_import,
            'named_range': func_named_range,
            }[s]


