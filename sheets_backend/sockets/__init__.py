import os
import pickle
import numpy
import traceback
import logging

import mysocket
import sheets_backend

logger = logging.getLogger(__name__)

class Packet(object): pass

class SetCell(Packet):
    def __init__(self, book_id, sheet_id, r, c, s):
        self.book_id = book_id
        self.sheet_id = sheet_id
        self.r = r
        self.c = c
        self.s = s
    
    def __call__(self, sock):
        book = sock.server.get_book(self.book_id)
        sheet = book.sheets[self.sheet_id]
        ret = sheet.set_cell(self.r, self.c, self.s)

        sock.send(pickle.dumps(Echo()))

        sock.server.save_book(self.book_id)

class SetScriptPre(Packet):
    def __init__(self, book_id, sheet_id, s):
        self.book_id = book_id
        self.sheet_id = sheet_id
        self.s = s
    
    def __call__(self, sock):
        book = sock.server.get_book(self.book_id)
        sheet = book.sheets[self.sheet_id]
        ret = book.set_script_pre(self.s)

        sock.send(pickle.dumps(Echo()))

        sock.server.save_book(self.book_id)

class AddColumn(Packet):
    def __init__(self, book_id, sheet_id, i):
        self.book_id = book_id
        self.sheet_id = sheet_id
        self.i = i
    
    def __call__(self, sock):
        book = sock.server.get_book(self.book_id)
        sheet = book.sheets[self.sheet_id]
        ret = sheet.add_column(self.i)
        sock.send(pickle.dumps(Echo()))

class AddRow(Packet):
    def __init__(self, book_id, sheet_id, i):
        self.book_id = book_id
        self.sheet_id = sheet_id
        self.i = i
    
    def __call__(self, sock):
        book = sock.server.get_book(self.book_id)
        sheet = book.sheets[self.sheet_id]
        ret = sheet.add_row(self.i)
        sock.send(pickle.dumps(Echo()))

class GetCellData(Packet):
    def __init__(self, book_id, sheet_id):
        self.book_id = book_id
        self.sheet_id = sheet_id
    
    def __call__(self, sock):
        book = sock.server.get_book(self.book_id)
        sheet = book.sheets[self.sheet_id]

        book.do_all()

        def f(c):
            if c is None:
                return sheets_backend.Cell('','')
            return sheets_backend.Cell(c.string,str(c.value))

        fv = numpy.vectorize(f, otypes=[sheets_backend.Cell])

        cells = fv(sheet.cells.cells)

        sock.send(pickle.dumps(ReturnCells(cells)))

def convert_cells(sheet):
        def f(c):
            if c is None:
                return sheets_backend.Cell('','')
            v = c.value
            if isinstance(v, str):
                v = "\"" + v + "\""
            else:
                v = str(v)
            return sheets_backend.Cell(c.string, v)

        fv = numpy.vectorize(f, otypes=[sheets_backend.Cell])

        return fv(sheet.cells.cells)

class GetSheetData(Packet):
    def __init__(self, book_id, sheet_id):
        self.book_id = book_id
        self.sheet_id = sheet_id
    
    def __call__(self, sock):
        book = sock.server.get_book(self.book_id)
        
        sheet = book.sheets[self.sheet_id]

        sock.send(pickle.dumps(ReturnSheetData(self.book_id, book, sheet)))

class RequestBookNew(Packet):
    def __init__(self): pass
    
    def __call__(self, sock):
        book_id, book = sock.server.storage.object_new()
        
        sheet = book.sheets["0"]

        #if not hasattr(sheet, 'script_output'):
        #    sheet.script_exec()

        res = ReturnSheetData(book_id, book, sheet)

        sock.send(pickle.dumps(res))

class ReturnSheetData(Packet):
    def __init__(self, book_id, book, sheet):

        book.do_all()

        self.book_id = book_id
        self.cells = convert_cells(sheet)
        
        self.script_pre = book.script_pre.string
        self.script_pre_output = book.script_pre.output
        self.script_post = book.script_post.string
        self.script_post_output = book.script_post.output

    def __call__(self, sock):
        pass

class ReturnCells(Packet):
    def __init__(self, cells):
        self.cells = cells
    def __call__(self, sock):
        pass

class Echo(Packet):
    def __init__(self):
        pass
    def __call__(self, sock):
        pass

class ClientSocket(mysocket.ClientSocket):
    def __init__(self, server, sock):
        mysocket.ClientSocket.__init__(self, server, sock)

    def do_recv(self, b):
        logger.debug('ClientSocket do_recv ' + repr(b))
        o = pickle.loads(b)
        logger.debug(o)
        try:
            o(self)
        except Exception as e:
            logger.exception('error processing packet ' + repr(o))

class Server(sheets_backend.Server, mysocket.Server):
    def __init__(self, storage, port):
        sheets_backend.Server.__init__(self, storage)
        mysocket.Server.__init__(self, '', port, ClientSocket)
    
    def run(self):
        logger.info('starting books server socket')
        mysocket.Server.run(self)

class Client(mysocket.Client):
    def __init__(self, port):
        mysocket.Client.__init__(self, '', port)

    def recv_packet(self):
        o = pickle.loads(self.recv())
        if not isinstance(o, Packet): raise TypeError()
        return o
    
    def book_new(self):
        self.send(pickle.dumps(RequestBookNew()))
        return self.recv_packet()
    
class BookProxy(sheets_backend.BookProxy, mysocket.Client):
    def __init__(self, book_id, port):
        mysocket.Client.__init__(self, '', port)
        self.book_id = book_id

    def recv_packet(self):
        o = pickle.loads(self.recv())
        if not isinstance(o, Packet): raise TypeError()
        return o

    def set_cell(self, k, r, c, s):
        self.send(pickle.dumps(SetCell(self.book_id, k, r, c, s)))
        return self.recv_packet()
    
    def set_script_pre(self, sheet_key, s):
        self.send(pickle.dumps(SetScriptPre(self.book_id, sheet_key, s)))
        return self.recv_packet()

    def get_sheet_data(self, sheet_key):
        self.send(pickle.dumps(GetSheetData(self.book_id, sheet_key)))
        return self.recv_packet()
    
    def get_cell_data(self, sheet_key):
        self.send(pickle.dumps(GetCellData(self.book_id, sheet_key)))
        return self.recv_packet()

    def add_column(self, sheet_key, i):
        self.send(pickle.dumps(AddColumn(self.book_id, sheet_key, i)))
        return self.recv_packet()

    def add_row(self, sheet_key, i):
        self.send(pickle.dumps(AddRow(self.book_id, sheet_key, i)))
        return self.recv_packet()


