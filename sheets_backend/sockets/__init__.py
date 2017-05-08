import os
import pickle
import numpy
import traceback

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

        sock.server.save_sheet(self.sheet_id)

class SetExec(Packet):
    def __init__(self, sheet_id, s):
        self.sheet_id = sheet_id
        self.s = s
    
    def __call__(self, sock):
        sheet = sock.server.get_sheet(self.sheet_id)
        ret = sheet.set_exec(self.s)

        sock.send(pickle.dumps(Echo()))

        sock.server.save_sheet(self.sheet_id)

class AddColumn(Packet):
    def __init__(self, sheet_id, i):
        self.sheet_id = sheet_id
        self.i = i
    
    def __call__(self, sock):
        sheet = sock.server.get_sheet(self.sheet_id)
        ret = sheet.add_column(self.i)
        print(ret)

        sock.send(pickle.dumps(Echo()))

class GetCellData(Packet):
    def __init__(self, sheet_id):
        self.sheet_id = sheet_id
    
    def __call__(self, sock):
        print('GetCellData.__call__')
        sheet = sock.server.get_sheet(self.sheet_id)
        
        def f(c):
            if c is None:
                return sheets_backend.Cell('','')
            return sheets_backend.Cell(c.string,str(c.value))

        fv = numpy.vectorize(f, otypes=[sheets_backend.Cell])

        cells = fv(sheet.cells)

        print(cells)

        sock.send(pickle.dumps(ReturnCells(cells)))

def convert_cells(sheet):
        def f(c):
            if c is None:
                return sheets_backend.Cell('','')
            return sheets_backend.Cell(c.string,str(c.value))

        fv = numpy.vectorize(f, otypes=[sheets_backend.Cell])

        return fv(sheet.cells)

class GetSheetData(Packet):
    def __init__(self, sheet_id):
        self.sheet_id = sheet_id
    
    def __call__(self, sock):
        sheet = sock.server.get_sheet(self.sheet_id)
        cells = convert_cells(sheet)

        if not hasattr(sheet, 'script_output'):
            sheet.script_exec()

        sock.send(pickle.dumps(ReturnSheetData(self.sheet_id, cells, sheet.script, sheet.script_output)))

class RequestSheetNew(Packet):
    def __init__(self): pass
    
    def __call__(self, sock):
        i, sheet = sock.server.storage.sheet_new()

        cells = convert_cells(sheet)

        if not hasattr(sheet, 'script_output'):
            sheet.script_exec()

        sock.send(pickle.dumps(ReturnSheetData(i, cells, sheet.script, sheet.script_output)))

class ReturnSheetData(Packet):
    def __init__(self, i, cells, script, script_output):
        self.i = i
        self.cells = cells
        self.script = script
        self.script_output = script_output
    def __call__(self, sock):
        print(self,sock)

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
        try:
            o(self)
        except Exception as e:
            print('error processing packet', repr(o))
            traceback.print_exc()

class Server(sheets_backend.Server, mysocket.Server):
    def __init__(self, storage):
        sheets_backend.Server.__init__(self, storage)
        mysocket.Server.__init__(self, '', int(os.environ['PORT_WEB_SHEETS_SOCKET']), ClientSocket)

class Client(mysocket.Client):
    def __init__(self):
        mysocket.Client.__init__(self, '', int(os.environ['PORT_WEB_SHEETS_SOCKET']))

    def recv_packet(self):
        o = pickle.loads(self.recv())
        if not isinstance(o, Packet): raise TypeError()
        return o
    
    def sheet_new(self):
        self.send(pickle.dumps(RequestSheetNew()))
        return self.recv_packet()
    
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
    
    def set_exec(self, s):
        self.send(pickle.dumps(SetExec(self.sheet_id, s)))
        return self.recv_packet()

    def get_sheet_data(self):
        self.send(pickle.dumps(GetSheetData(self.sheet_id)))
        return self.recv_packet()
    
    def get_cell_data(self):
        self.send(pickle.dumps(GetCellData(self.sheet_id)))
        return self.recv_packet()

    def add_column(self, i):
        self.send(pickle.dumps(AddColumn(self.sheet_id, i)))
        return self.recv_packet()


