import sys
import json
import logging
import logging.config
import argparse

import storage.filesystem
import sheets
import sheets_backend.sockets

import unittest

class Test(unittest.TestCase):
    def test(argv):
        
        sys.path.insert(0, './testing')
    
        settings_module = __import__('web_sheets_sheets_backend.settings', fromlist=['*'])
        
        port = settings_module.PORT
        
        client = sheets_backend.sockets.Client(port)
        
        print(client.book_new())
    
    
    
    
    
    
