import sys
import json
import logging
import logging.config

import storage.filesystem
import sheets
import sheets_backend.sockets

def test():
    sys.path.insert(0, '/etc/web_sheets_sheets_backend')
    settings_module = __import__('web_sheets_sheets_backend.settings', fromlist=['*'])

    logging.config.dictConfig(settings_module.LOGGING)

    port = settings_module.PORT
    
    folder = settings_module.STORAGE_FOLDER
    
    stor = storage.filesystem.Storage(sheets.Book, folder)

    server = sheets_backend.sockets.Server(stor, port)
    
    server.run()

def daemon():
    logger = logging.getLogger(__name__)
    try:
        test()
    except:
        logger.exception('exception occured')

