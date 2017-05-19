import sys
import json
import logging
import logging.config
import argparse

import storage.filesystem
import sheets
import sheets_backend.sockets

import unittest

class TestClient(unittest.TestCase):
    def test(argv):
    
        print(sys.path)

        sys.path.insert(0, './testing')
    
        settings_module = __import__('web_sheets_sheets_backend.settings', fromlist=['*'])
        
        port = settings_module.PORT

        print(sys.path)
    
        print(settings_module)

        print("start client on port {}".format(port))
        
        client = sheets_backend.sockets.Client(port)
        
        print(client.book_new())
    
    
    
    
    
    
