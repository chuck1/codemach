import sys
import json
import logging
import logging.config
import argparse

import storage.filesystem
import sheets
import sheets.tests.settings
import sheets_backend.sockets

import modconf

def test(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument(
            'conf_dir',
            help='modconf module directory')
    parser.add_argument(
            'conf_mod',
            help='modconf module name')

    args = parser.parse_args(argv)
    
    conf = modconf.import_conf(args.conf_name, args.conf_dir)

    logging.config.dictConfig(conf.LOGGING)

    stor = storage.filesystem.Storage(
            sheets.Book, 
            conf.STORAGE_FOLDER)

    stor.set_object_new_args(
            (conf.sheets_conf.Settings,))

    server = sheets_backend.sockets.Server(stor, conf.PORT)
    
    server.run()

def daemon(argv):
    logger = logging.getLogger(__name__)
    try:
        test(argv)
    except:
        logger.exception('exception occured')





