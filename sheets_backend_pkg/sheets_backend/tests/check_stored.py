import os
import sys
import json
import logging
import logging.config

import unittest

import storage.filesystem
import sheets
import sheets_backend.sockets

class TestCheckStored(unittest.TestCase):
    def test(self):
        sys.path.insert(0, './testing')
        settings_module = __import__('web_sheets_sheets_backend.settings', fromlist=['*'])
    
        #logging.config.dictConfig(settings_module.LOGGING)
    
        #port = settings_module.PORT
        
        folder = settings_module.STORAGE_FOLDER_PRODUCTION
        
        stor = storage.filesystem.Storage(sheets.Book, folder)
    
        #server = sheets_backend.sockets.Server(stor, port)
    
        #return stor
        
        lst = os.listdir(stor.folder)
    
        print('files:',lst)
    
        for f in lst:
            h, t = os.path.splitext(f)
            if t == '.bin':
                try:
                    o = stor.read(h)
                    print(repr(o))
                    print(dir(o))
                except Exception as e:
                    print(e)
    
                print()
    
