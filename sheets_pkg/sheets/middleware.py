
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

    def call_cell_eval(self, book, cell, code, _globals, res):
        """
        .. DANGER::
           the middleware objects are responsible for setting the appropriate
           context before evaluation of code
        """
        pass

class SecurityGlobalsResult(object):
    def __init__(self):
        self._globals = {'__builtins__': {}}

class SecurityEvalResult(object):
    pass

class SecurityExecResult(object):
    pass

class MiddlewareSecurityManager(object):
    def __init__(self, classes):
        self.objects = list()
        for m,c in classes:
            m = __import__(m, fromlist=[c])
            self.objects.append(getattr(m,c)())
    
    def call_book_globals(self, book):
        res = SecurityGlobalsResult()
        for o in self.objects:
            o.call_book_globals(book, res)
        return res

    def call_sheet_globals(self, book, sheet):
        res = SecurityGlobalsResult()
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
   
    def call_cell_eval(self, book, cell, code, _globals):
        res = SecurityEvalResult()
        for o in self.objects:
            o.call_cell_eval(book, cell, code, _globals, res)
        return res

    def call_script_exec(self, book, script, code, _globals):
        res = SecurityExecResult()
        for o in self.objects:
            o.call_script_exec(book, script, code, _globals, res)
        return res


