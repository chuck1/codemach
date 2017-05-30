import os
import pickle
import numpy
import traceback
import logging

import mysocket
import sheets_backend

logger = logging.getLogger(__name__)

class Packet(object):
    def __call__(self, sock):
        pass

class PacketException(object):
    def __init__(self, message):
        self.message = message
    def __call__(self, sock):
        pass

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

        sock.send(pickle.dumps(Packet()))

        sock.server.save_book(self.book_id)

class SetDocs(Packet):
    def __init__(self, book_id, s):
        self.book_id = book_id
        self.s = s
    
    def __call__(self, sock):
        book = sock.server.get_book(self.book_id)
        
        book.set_docs(self.s)

        sock.send(pickle.dumps(Packet()))

        sock.server.save_book(self.book_id)

class SetScriptPre(Packet):
    def __init__(self, book_id, s):
        self.book_id = book_id
        self.s = s
    
    def __call__(self, sock):
        book = sock.server.get_book(self.book_id)
        
        ret = book.set_script_pre(self.s)

        sock.send(pickle.dumps(Packet()))

        sock.server.save_book(self.book_id)

class SetScriptPost(Packet):
    def __init__(self, book_id, s):
        self.book_id = book_id
        self.s = s
    
    def __call__(self, sock):
        book = sock.server.get_book(self.book_id)

        ret = book.set_script_post(self.s)

        sock.send(pickle.dumps(Packet()))

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
        sock.send(pickle.dumps(Packet()))

class AddRow(Packet):
    def __init__(self, book_id, sheet_id, i):
        self.book_id = book_id
        self.sheet_id = sheet_id
        self.i = i
    
    def __call__(self, sock):
        book = sock.server.get_book(self.book_id)
        sheet = book.sheets[self.sheet_id]
        ret = sheet.add_row(self.i)
        sock.send(pickle.dumps(Packet()))

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

class GetScriptPostOutput(Packet):
    def __init__(self, book_id):
        self.book_id = book_id
    
    def __call__(self, sock):
        book = sock.server.get_book(self.book_id)
        
        sock.send(pickle.dumps(ReturnScriptPostOutput(self.book_id, book)))

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
        
        self.docs = book.docs
        self.script_pre = book.script_pre.string
        self.script_pre_output = book.script_pre.output
        self.script_post = book.script_post.string
        self.script_post_output = book.script_post.output

class ReturnScriptPostOutput(Packet):
    def __init__(self, book_id, book):

        book.do_all()
        
        self.script_post_output = book.script_post.output

class ReturnCells(Packet):
    def __init__(self, cells):
        self.cells = cells
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
            self.send(pickle.dumps(PacketException(str(e))))

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
        b = self.recv()
        o = pickle.loads(b)
        if not isinstance(o, Packet):
            logger.error('bytes:',repr(b))
            raise TypeError()
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

    def send_recv_packet(self, packet):
        self.send(pickle.dumps(packet))
        return self.recv_packet()

    def set_docs(self, s):
        return self.send_recv_packet(SetDocs(self.book_id, s))

    def set_cell(self, k, r, c, s):
        return self.send_recv_packet(SetCell(self.book_id, k, r, c, s))
    
    def set_script_pre(self, s):
        self.send(pickle.dumps(SetScriptPre(self.book_id, s)))
        return self.recv_packet()

    def set_script_post(self, s):
        self.send(pickle.dumps(SetScriptPost(self.book_id, s)))
        return self.recv_packet()

    def get_sheet_data(self, sheet_key):
        self.send(pickle.dumps(GetSheetData(self.book_id, sheet_key)))
        return self.recv_packet()

    def get_script_post_output(self):
        self.send(pickle.dumps(GetScriptPostOutput(self.book_id)))
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


