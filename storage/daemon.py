
import logging
import logging.config

import storage.filesystem

def test():

    settings = json.loads(open('/etc/web_sheets_storage/settings.json', 'r').read())

    logging.config.dictConfig({
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
        })

    port = settings.get('port',10001)

    #stor = storage.filesystem.Storage(settings.get('storage_folder', '/etc/web_sheets_sheets_backend/storage'))

    #server = sheets_backend.sockets.Server(stor, port)
    
    #server.run()

def daemon():
    logger = logging.getLogger(__name__)
    try:
        test()
    except:
        logger.exception('exception occured')



