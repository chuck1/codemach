
class MiddleWareSecurity(object):
    """
    Security middleware is used to remove the details of
    security-related functionality from the core classes

    The following security related functions are performed by
    a MiddleWareSecurity object

    - populate book globals
    - populate sheet globals
    - analyze compiled user code
    - analyze calls to core class methods during execution of user code

    """
    def call_book_globals(self, book, res):
        pass

    def call_sheet_globals(self, book, sheet, res):
        pass

    def call_book_method_decorator(self, book, f, args):
        pass

class MiddlewareSecurityResult(object):
    def __init__(self):
        self._globals = {'__builtins__': {}}

class MiddlewareSecurityManager(object):
    def __init__(self, classes):
        self.objects = list()
        for m,c in classes:
            m = __import__(m, fromlist=[c])
            self.objects.append(getattr(m,c)())
    
    def call_book_globals(self, book):
        res = MiddlewareSecurityResult()
        for o in self.objects:
            o.call_book_globals(book, res)
        return res

    def call_sheet_globals(self, book, sheet):
        res = MiddlewareSecurityResult()
        for o in self.objects:
            o.call_sheet_globals(book, sheet, res)
        return res

    def call_book_method_decorator(self, book, f, args):
        for o in self.objects:
            o.call_book_method_decorator(book, f, args)

    def call_check_cell_code(self, cell):
        for o in self.objects:
            o.call_check_cell_code(cell)

    def call_check_script_code(self, script):
        for o in self.objects:
            o.call_check_script_code(script)
   



