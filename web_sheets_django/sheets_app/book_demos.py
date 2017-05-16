
def func_import(bp):

    bp.set_script_pre('0', 'import math\nprint(math)\n')

    bp.set_cell('0', 0, 0, 'math.pi')

def get_func(s):
    
    return {
            'import': func_import
            }[s]


