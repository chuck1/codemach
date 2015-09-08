import os
import array
import xml.etree.ElementTree as et
import pickle
import re
import numpy as np
import struct
import signal
import datetime

import python_spreadsheet as ss
import python_spreadsheet.sheet
import python_spreadsheet.security

name_srv_w = "/tmp/python_spreadsheet_srv_w"
name_cli_w = "/tmp/python_spreadsheet_cli_w"

def cli_read():
    with open(name_srv_w, 'rb') as f:
        return f.read()

def cli_write(s):
    with open(name_cli_w, 'wb') as f:
        f.write(s)


class Request(object):
    def __init__(self, s, usr=None):
        self.s = s
        self.usr = usr

    def do(self):
        cli_write(pickle.dumps(self))

        self.res = cli_read()

class Stop(Exception):
    pass

class Service(object):
    def __init__(self):
        try:
            self.load()
            print "sheets loaded"
        except:
            self.sheets = {}
            print "sheets not loaded"

        self.fifo_name_srv_w = "/tmp/python_spreadsheet_srv_w"
        self.fifo_name_cli_w = "/tmp/python_spreadsheet_cli_w"

        def signal_handler(signum, frame):
            print 'signal handler called with signal', signum
            if (signum == signal.SIGTERM) or (signum == signal.SIGINT):
                self.save()

        signal.signal(signal.SIGTERM, signal_handler)
        signal.signal(signal.SIGINT,  signal_handler)
        

        try:
            os.remove(self.fifo_name_srv_w)
            print self.fifo_name_srv_w, "removed"
            os.remove(self.fifo_name_cli_w)
            print self.fifo_name_cli_w, "removed"
        except Exception as e:
            print e
            pass

        try:
            um = os.umask(000)
            print "umask was",um
            os.mkfifo(self.fifo_name_srv_w, 0777)
            print self.fifo_name_srv_w, "created"
            os.mkfifo(self.fifo_name_cli_w, 0777)
            print self.fifo_name_cli_w, "created"
            os.umask(um)
        except OSError:
            pass

    def save(self):
        fn = os.path.join(os.path.dirname(__file__),'data','sheets.bin')
        with open(fn, 'wb') as f:
            pickle.dump(self.sheets, f)

    def load(self):
        fn = os.path.join(os.path.dirname(__file__),'data','sheets.bin')
        with open(fn, 'rb') as f:
            self.sheets = pickle.load(f)

    def write(self, s):
        with open(self.fifo_name_srv_w, 'wb') as f:
            f.write(s)
    
    def read(self):
        with open(self.fifo_name_cli_w, 'rb') as f:
            return f.read()

    def parse_cell(self, s):
        m = re.match('^(\d+)_(\d+)$', s)
        r = int(m.group(1))
        c = int(m.group(2))
        return r,c

    def blocking_read(self):
        #a = array.array('i')

        s = self.read()
        req = pickle.loads(s)
        #a.fromstring(s)
    
        print 'req.s =',req.s
        
        if req.usr:
            # get or create sheet for user
            try:
                sheet = self.sheets[req.usr]
            except:
                sheet = ss.sheet.Sheet()
                self.sheets[req.usr] = sheet
            
        

            if req.s == 'get sheet':
                s_out = pickle.dumps(sheet)
                self.write(s_out)

            elif req.s == 'add row':
                sheet.add_row()
                self.write('0')
        
            elif req.s == 'add col':
                sheet.add_col()
                self.write('0')

            elif req.s == 'set cell':
                #cell = self.read()
                #text = self.read()
                #print 'cell =',cell,'text =',text
            
                cell = req.cell
                text = req.text
            
                self.write('0')
           
                print 'cell =',cell
                print 'text =',text

                r,c = self.parse_cell(cell)

                print 'r,c = ',r,c
      
                sheet.set_cell(r, c, text)
            else:
                self.write('unknown command')

        elif req.s == 'login':
            u = req.u
            p = req.p
            
            print 'usr',u
            print 'pwd',p

            try:
                ss.security.check_pwd(u,p)
            except ss.security.InvalidUsr:
                print 'invalid usr'
                ss.security.create_usr(u,p)
                self.write('login success')
            except ss.security.InvalidPwd:
                print 'invalid pwd'
                self.write('invalid pwd')
            else:
                print 'success'
                self.write('login success')
        elif req.s == 'stop':
            self.write('0')
            raise Stop()
        else:
            raise ValueError("unknown command or forgot to set req.usr. req.s = {}".format(
                repr(req.s)))

        #print a

    def run(self):
        
        t = datetime.datetime.now() + datetime.timedelta(minutes=1)
        
        while True:
            # save every minute
            if datetime.datetime.now() > t:
                self.save()
                t = datetime.datetime.now() + datetime.timedelta(minutes=1)

            try:
                self.blocking_read()
            except Stop:
                break
            except IOError:
                print "got ioerror"
                break


