


MIDDLEWARE_SECURITY = (
        ('sheets.ext.middleware.security','SecurityTest1'),
        )

MIDDLEWARE_SECURITY_MODULES_APPROVED = (
        "math",
        "numpy",
        "time",
        )

MIDDLEWARE_SECURITY_BUILTINS_APPROVED = {
        '__build_class__': __build_class__,
        '__name__': 'module',
        "Exception": Exception,
        'dir': dir,
        'globals': globals,
        'list': list,
        'object': object,
        'print': print,
        'range': range,
        "repr": repr,
        'sum': sum,
        "type": type,
        }


