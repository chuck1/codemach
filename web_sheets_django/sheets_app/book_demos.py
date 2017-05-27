
import sheets.tests.functions

DEMOS = {
            'import': sheets.tests.functions.TestImport,
            'named_range': sheets.tests.functions.TestNamedRange,
            'sum': sheets.tests.functions.TestSum,
            'indexof': sheets.tests.functions.TestIndexof,
            'lookup': sheets.tests.functions.TestLookup,
            'datetime': sheets.tests.functions.TestDatetime,
            'string': sheets.tests.functions.TestStrings,
            'math': sheets.tests.functions.TestMath,
            'numericaltypes': sheets.tests.functions.TestNumericalTypes,
            }

def get_func(s):
    
    return DEMOS[s]





