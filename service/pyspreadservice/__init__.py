import os
import array
import xml.etree.ElementTree as et
import pickle
import re
import numpy as np
import struct
import signal
import datetime
import random

import mysock

import sheet

server_port = 9000

def parse_cell(s):
    m = re.match('^(\d+)_(\d+)$', s)
    r = int(m.group(1))
    c = int(m.group(2))
    return r,c

class Request(object):
    def __init__(self, session_id):
        self.session_id = session_id

    def get_session(self, service, sock):

        try:
            return service.sessions[self.session_id]
        except KeyError as e:
            return self.on_get_session_error(service, sock, e)

    def on_get_session_error(self, service, sock, err):
        print "error", repr(err), repr(err.message)
        send_response(sock, ResponseError(err.message))
        return None
    
    def on_session_recv(self, sock, session):
        pass

class RequestSheet(Request):
    def __init__(self, session_key, sheet_filename):
        super(RequestSheet, self).__init__(session_key)
        self.sheet_filename = sheet_filename
        
    def on_get_session_error(self, service, sock, err):
        print "error", repr(err), repr(err.message)

        try:
            return service.create_session(self.session_id, self.sheet_filename)
        except Exception as e:
            print "send error", repr(e), repr(e.message)
            send_response(sock, ResponseError(e.message))
            return None

    def on_session_recv(self, sock, session):
        send_response(sock, ResponseSheet(session.session_id, session.sheet))


class RequestCellSet(Request):
    def __init__(self, session_key):
        super(RequestCellSet, self).__init__(session_key)

    def on_session_recv(self, sock, session):

        print 'cell =', self.cell
        print 'text =', self.text

        r, c = self.cell

        print 'r,c = ', r, c
      
        session.sheet.set_cell(r, c, self.text)

        send_response(sock, ResponseSheet(session.session_id, session.sheet))

        session.sheet_save()

class RequestSheetAddRow(Request):
    def __init__(self, session_key):
        super(RequestSheetAddRow, self).__init__(session_key)

    def on_session_recv(self, sock, session):
        
        session.sheet.add_row()

        send_response(sock, ResponseSheet(session.session_id, session.sheet))

        session.sheet_save()


class Response(object):
    pass

class ResponseError(Response):
    def __init__(self, message):
        self.message = message


class ResponseSheet(Response):
    def __init__(self, session_id, sheet):
        self.session_id = session_id
        self.sheet = sheet

    


class Session(object):
    def __init__(self, session_key, sheet_filename):
        self.session_id = session_key
        self.sheet_filename = sheet_filename
        
        self.sheet_load()
       
    def sheet_fullpath(self):
        return os.path.join(os.path.dirname(__file__),'data','sheets',self.sheet_filename)

    def sheet_load(self):
        try:
            with open(self.sheet_fullpath(), 'rb') as f:
                self.sheet = pickle.load(f)
        except IOError as e:
            print "sheet doesnt exist, creating new sheet", repr(self.sheet_filename)
            self.sheet = sheet.Sheet()

    def sheet_save(self):
        print "saving sheet", repr(self.sheet_filename)

        with open(self.sheet_fullpath(), 'wb') as f:
            pickle.dump(self.sheet, f)

class SocketServer(mysock.Server):

    def __init__(self, service, host, port):
        super(SocketServer, self).__init__(host, port)

        self.service = service

    def on_recv(self):
        # self.s
        # self.data

        self.service.on_recv(self.s, self.data)
    
class SocketClient(mysock.Client):

    def __init__(self):
        super(SocketClient, self).__init__()

    def connect2(self):
        self.connect("localhost", server_port)

def send_response(sock, res):
    sock.send(pickle.dumps(res))

def send_request(req):
    client = SocketClient()
    client.connect2()

    client.send(pickle.dumps(req))

    data = client.recv()

    print "client received", repr(data)

    response = pickle.loads(data)

    return response

class Server(object):
    def __init__(self):

        self.socketserver = SocketServer(self, "", server_port)

        
        self.sessions = {}
 
        """
        self.logfile = f

        def signal_handler(signum, frame):
            print 'signal handler called with signal', signum
            if (signum == signal.SIGTERM) or (signum == signal.SIGINT):
                self.save()
                self.f.close()

        signal.signal(signal.SIGTERM, signal_handler)
        signal.signal(signal.SIGINT,  signal_handler)

        """


    def create_session(self, session_key, sheet_filename):
        
        for s in self.sessions:
            if s.sheet_filename == sheet_filename:
                raise Exception("sheet already open")

        s = Session(session_key, sheet_filename)
        self.sessions[s.session_id] = s
        
        print "created session {} {}".format(repr(s.session_id), repr(sheet_filename))

        return s

    def on_recv(self, sock, data):
        
        req = pickle.loads(data)
    
        print "req.session_id =", req.session_id

        session = req.get_session(self, sock)

        if session is None: return


        print "session found"
        
        req.on_session_recv(sock, session)


        """

            elif req.s == 'add row':
                sheet.add_row()
                self.write('0')
        
            elif req.s == 'add col':
                sheet.add_col()
                self.write('0')

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
                
                sess = self.create_session(u)

                self.write("login success,{}".format(sess.sessid))
            except ss.security.InvalidPwd:
                print 'invalid pwd'
                self.write('invalid pwd')
            else:
                # create new session
                sess = self.create_session(u)
                print 'success'
                self.write("login success,{}".format(sess.sessid))

        elif req.s == 'stop':
            self.write('0')
            raise Stop()
        else:
            err_str  = "unknown command or forgot to "
            err_str += "set req.usr. req.s = {}".format(repr(req.s))

            self.write('error:' + err_str)

        """

    def main_loop(self):

        print "main loop"

        t = datetime.datetime.now() + datetime.timedelta(minutes=1)
       
        self.socketserver.main_loop()

        while True:
            # save every minute
            if datetime.datetime.now() > t:
                self.save()
                t = datetime.datetime.now() + datetime.timedelta(minutes=1)

            try:
                print "waiting for data"
                self.blocking_read()
            except Stop:
                break
            except IOError:
                print "got ioerror"
                break




