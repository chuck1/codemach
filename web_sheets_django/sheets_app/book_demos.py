
import sheets.tests.functions

DEMOS = {
            'import': sheets.tests.functions.func_import,
            'named_range': sheets.tests.functions.func_named_range,
            'sum': sheets.tests.functions.func_sum,
            'indexof': sheets.tests.functions.func_indexof,
            'lookup': sheets.tests.functions.func_lookup,
            'datetime': sheets.tests.functions.func_datetime,
            }

def get_func(s):
    
    return DEMOS[s]





