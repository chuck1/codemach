import sys
import json
import argparse
import modconf
import sheets
import sheets_backend.sockets
import subprocess
import unittest

class TestClient(unittest.TestCase):

    def setUp(self):
        self.conf_mod = 'sheets_backend.tests.conf.simple'

        self.p = subprocess.Popen(('web_sheets_sheets_backend.py', self.conf_mod))

    def tearDown(self):
        self.p.kill()

    def test(self):
    
        conf = modconf.import_conf(self.conf_mod)

        port = conf.PORT
        
        print("connect on port {}".format(port))
        
        client = sheets_backend.sockets.Client(port)
        
        print(client.book_new())
    
    
    
    
    
    
