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

class RequestSheetShowFormula(Request):
    def __init__(self, session_key):
        super(RequestSheetAddRow, self).__init__(session_key)

    def on_session_recv(self, sock, session):
        
        session.sheet.add_row()

        send_response(sock, ResponseSheet(session.session_id, session.sheet))

        session.sheet_save()

















