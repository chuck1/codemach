
import json
import logging
import logging.config

import storage.filesystem
import sheets
import sheets_backend.sockets

def test():

    settings = json.loads(open('/etc/web_sheets_sheets_backend/settings.json', 'r').read())

    logging.config.dictConfig({
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'file': {
                'level': 'DEBUG',
                'class': 'logging.FileHandler',
                'filename':'/var/log/web_sheets_sheets_backend/debug.log',
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
        })

    port = settings.get('port',10002)
    folder = settings.get('storage_folder', '/etc/web_sheets_sheets_backend/storage')
    
    cls = sheets.Book

    stor = storage.filesystem.Storage(cls, folder)

    server = sheets_backend.sockets.Server(stor, port)
    
    server.run()

def daemon():
    logger = logging.getLogger(__name__)
    try:
        test()
    except:
        logger.exception('exception occured')

