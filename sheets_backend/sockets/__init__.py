import os
import pickle
import numpy

import mysocket
import sheets_backend

class Packet(object):pass

class SetCell(Packet):
    def __init__(self, sheet_id, r, c, s):
        self.sheet_id = sheet_id
        self.r = r
        self.c = c
        self.s = s
    
    def __call__(self, sock):
        print('SetCell.__call__')
        sheet = sock.server.get_sheet(self.sheet_id)
        ret = sheet.set_cell(self.r, self.c, self.s)
        print(ret)

        sock.send(pickle.dumps(Echo()))

class GetCellData(Packet):
    def __init__(self, sheet_id):
        self.sheet_id = sheet_id
    
    def __call__(self, sock):
        print('GetCellData.__call__')
        sheet = sock.server.get_sheet(self.sheet_id)
        
        def f(c):
            return sheets_backend.Cell(c.string,str(c.value))

        fv = numpy.vectorize(f)

        cells = fv(sheet.cells)

        print(cells)

        sock.send(pickle.dumps(ReturnCells(cells)))

class ReturnCells(Packet):
    def __init__(self, cells):
        self.cells = cells
    def __call__(self, sock):
        print(self,sock)

class Echo(Packet):
    def __init__(self):
        pass
    def __call__(self, sock):
        print('Echo',sock)

class ClientSocket(mysocket.ClientSocket):
    def __init__(self, server, sock):
        mysocket.ClientSocket.__init__(self, server, sock)

    def do_recv(self, b):
        print('sheets_backend.sockets.ClientSocket do_recv',repr(b))

        o = pickle.loads(b)

        print(o)

        o(self)


class Server(sheets_backend.Server, mysocket.Server):
    def __init__(self, storage):
        sheets_backend.Server.__init__(self, storage)
        mysocket.Server.__init__(self, '', int(os.environ['PORT_WEB_SHEETS_SOCKET']), ClientSocket)
    
class SheetProxy(sheets_backend.SheetProxy, mysocket.Client):
    def __init__(self, sheet_id):
        mysocket.Client.__init__(self, '', int(os.environ['PORT_WEB_SHEETS_SOCKET']))
        self.sheet_id = sheet_id

    def recv_packet(self):
        o = pickle.loads(self.recv())
        if not isinstance(o, Packet): raise TypeError()
        return o

    def set_cell(self, r, c, s):
        self.send(pickle.dumps(SetCell(self.sheet_id, r, c, s)))
        return self.recv_packet()

    def get_cell_data(self):
        self.send(pickle.dumps(GetCellData(self.sheet_id)))
        return self.recv_packet()




