
class Settings(object):
    
    MIDDLEWARE_SECURITY = (
            ('sheets.ext.middleware.security','SecurityTest1'),
            )
    
    MIDDLEWARE_SECURITY_MODULES_APPROVED = (
            "math",
            "numpy",
            "time",
            )
    
    MIDDLEWARE_SECURITY_BUILTINS_APPROVED = (
            '__build_class__',
            '__name__',
            "Exception",
            'dir',
            'getattr',
            'globals',
            'list',
            'object',
            'print',
            'range',
            "repr",
            'sum',
            "type",
            )
    

