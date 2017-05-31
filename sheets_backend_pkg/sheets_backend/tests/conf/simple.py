import modconf

conf_sheets = modconf.import_conf('sheets.tests.conf.simple')

LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'file': {
                'level': 'DEBUG',
                'class': 'logging.FileHandler',
                'filename':'venv/testing/log/web_sheets_sheets_backend/debug.log',
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

PORT = 10003

STORAGE_FOLDER = 'venv/testing/web_sheets_sheets_backend/storage'

STORAGE_FOLDER_PRODUCTION = '/etc/web_sheets_sheets_backend/storage'

