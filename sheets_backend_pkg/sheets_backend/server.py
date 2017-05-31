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
            '--conf_dir',
            nargs=1,
            default=(None,),
            help='modconf module directory')
    parser.add_argument(
            'conf_mod',
            help='modconf module name')
    
    args = parser.parse_args(argv[1:])
    
    conf = modconf.import_conf(args.conf_mod, args.conf_dir[0])

    logging.config.dictConfig(conf.LOGGING)

    stor = storage.filesystem.Storage(
            sheets.Book, 
            conf.STORAGE_FOLDER)

    stor.set_object_new_args(
            (conf.conf_sheets.Settings,))

    server = sheets_backend.sockets.Server(stor, conf.PORT)
    
    server.run()

def main(argv):
    logger = logging.getLogger(__name__)
    try:
        test(argv)
    except:
        logger.exception('exception occured')





