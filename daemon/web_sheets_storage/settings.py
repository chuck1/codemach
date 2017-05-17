
LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'file': {
                'level': 'DEBUG',
                'class': 'logging.FileHandler',
                'filename':'/var/log/web_sheets_storage/debug.log',
                'formatter':'basic'
                },
            },
        'loggers': {
            '__main__': {
                'handlers': ['file'],
                'level': 'DEBUG',
                'propagate': True,
                },
            'sheets_backend': {
                'handlers': ['file'],
                'level': 'DEBUG',
                'propagate': True,
                },
            },
        'formatters': {
            "basic":{
                "format":"%(asctime)s %(module)s %(levelname)s %(message)s"
                }
            }
        }

PORT = 10001

