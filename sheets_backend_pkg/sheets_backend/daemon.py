import sys
import json
import logging
import logging.config
import argparse

import storage.filesystem
import sheets
import sheets.tests
import sheets_backend.sockets

def test(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument(
            '--settings',
            nargs=1,
            default=['/etc/web_sheets_sheets_backend'],
            help='settings module directory')
    
    args = parser.parse_args(argv)
    
    settings_module_dir = args.settings[0]

    sys.path.insert(0, settings_module_dir)

    settings_module = __import__('web_sheets_sheets_backend.settings', fromlist=['*'])

    settings_module_sheets = sheets.tests.settings

    logging.config.dictConfig(settings_module.LOGGING)

    port = settings_module.PORT
    
    folder = settings_module.STORAGE_FOLDER
    
    stor = storage.filesystem.Storage(sheets.Book, folder)
    stor.set_object_new_args((settings_module_sheets,))

    server = sheets_backend.sockets.Server(stor, port)
    
    server.run()

def daemon(argv):
    logger = logging.getLogger(__name__)
    try:
        test(argv)
    except:
        logger.exception('exception occured')





