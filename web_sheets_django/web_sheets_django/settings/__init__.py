
from web_sheets_django.settings.base import *

DEBUG = False


LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'file': {
                'level': 'DEBUG',
                'class': 'logging.FileHandler',
                'filename': '/home/chuck/git/web_sheets/web_sheets_django/debug.log',
                },
            },
        'loggers': {
            'django': {
                'handlers': ['file'],
                'level': 'DEBUG',
                'propagate': True,
                },
            },
        }

