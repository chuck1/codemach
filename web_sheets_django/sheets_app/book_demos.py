
import sheets.tests.functions

def get_func(s):
    
    return {
            'import': sheets.tests.functions.func_import,
            'named_range': sheets.tests.functions.func_named_range,
            'sum': sheets.tests.functions.func_sum,
            'indexof': sheets.tests.functions.func_indexof,
            }[s]





