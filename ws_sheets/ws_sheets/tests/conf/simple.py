
class Settings(object):
    """
    these config variables must be stored in a class because I want
    to pickle the Book.settings variable with the book and
    modules cannot be pickled
    """
    
    MIDDLEWARE_SECURITY = (
            ('sheets.ext.middleware.security','SecurityTest1'),
            )
    
    MIDDLEWARE_SECURITY_MODULES_APPROVED = (
            "math",
            "numpy",
            "time",
            "datetime",
            "pytz",
            )
    
    MIDDLEWARE_SECURITY_BUILTINS_APPROVED = (
            '__build_class__',
            '__name__',
            'abs',
            'complex',
            'dir',
            'divmod',
            'Exception',
            'float',
            'getattr',
            'globals',
            'int',
            'list',
            'object',
            'pow',
            'print',
            'range',
            'repr',
            'sum',
            'type',
            )
    

