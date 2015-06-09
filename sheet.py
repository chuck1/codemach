import os
import array
import xml.etree.ElementTree as et
import pickle
import re
import numpy as np
import md5
import struct
import signal
import datetime

name_srv_w = "/tmp/python_spreadsheet_srv_w"
name_cli_w = "/tmp/python_spreadsheet_cli_w"

def cli_read():
    with open(name_srv_w, 'rb') as f:
        return f.read()

def cli_write(s):
    with open(name_cli_w, 'wb') as f:
        f.write(s)


def strhex(s):
    return " ".join("{:02x}".format(ord(c)) for c in s)

def match_int(s):
    return re.match('^\d+$', s)

def match_float(s):
    m1 = re.match('^\d+\.\d*$', s)
    m2 = re.match('^\d*\.\d+$', s)

    if m1:
        return m1
    elif m2:
        return m2
    else:
        return None


class Cell(object):
    def __init__(self, s=None):
        self.set_value(s)

    def set_value(self, s):
        if not s:
            self.dtype = 'none'
            self.v = None
        else:
            if s[0] == '=':
                self.dtype = 'formula'
                self.v = s
            else:
                m = match_int(s)
                if m:
                    self.dtype = 'int'
                    self.v = int(s)
                else:
                    m = match_float(s)
                    if m:
                        self.dtype = 'float'
                        self.v = float(s)
                    else:
                        self.dtype = 'str'
                        self.v = s

    def get_value(self, sheet):
        if self.dtype == 'formula':
            #func_cell = lambda r,c: sheet.get_cell(r,c).get_value(sheet)
            func_cell = lambda r,c: sheet.get_cell_value(r,c)
            _globals = {'cell':func_cell}
            return eval(self.v[1:], _globals)
        else:
            return self.v
    
    def str_type(self):
        return str(self.dtype)

    def str_value(self, sheet):
        return str(self.get_value(sheet))

class Sheet(object):
    def __init__(self):
        self.table = np.array([[Cell()]])
        #self.table = np.array([[Cell()]], dtype=Cell)

    def add_row(self):
        l = np.shape(self.table)[1]
        
        a = [[None]*l]

        for r in range(1):
            for c in range(l):
                a[r][c] = Cell()
                a[r][c].set_value(None)

        self.table = np.append(self.table, a, axis=0)

    def add_col(self):
        l = np.shape(self.table)[0]

        a = np.empty((l,1), dtype=Cell)

        for r in range(l):
            for c in range(1):
                a[r,c] = Cell()
                a[r,c].set_value(None)

        self.table = np.append(self.table, a, axis=1)

    def set_cell(self, r, c, v):
        while len(self.table) <= r:
            self.add_row()
        
        while np.shape(self.table)[1] <= c:
            self.add_col()

        self.table[r][c].set_value(v)
        
    def get_cell(self, r, c):
        try:
            row = self.table[r]
        except IndexError as e:
            return "row index error"
        
        try:
            col = row[c]
        except IndexError as e:
            return "col index error"
        
        return col

    def get_cells(self,r,c):
        try:
            return self.table[r,c]
        except:
            return "index error"

    def get_cell_value(self, r, c):
        if isinstance(r, int) and isinstance(c, int):
            return self.get_cell(r,c).get_value(self)
        else:
            cells = self.get_cells(r,c)

            f = np.vectorize(lambda c: c.get_value(self))
            
            #print "vectorize"
            #print cells

            try:
                a = f(cells)
                return a
            except TypeError:
                return "TypeError"
            except ValueError:
                return "ValueError"

    def html_col(self, row, r, c, func):

        td = 0
        td = et.Element('td')
        
        form = et.SubElement(td, 'form', attrib={'id':"form{}_{}".format(r,c)})
        
        t = et.SubElement(form, 'input', attrib={
            'id'  :"{}_{}".format(r,c),
            'type':"text",
            'name':"text"
            })
        
        h = et.SubElement(form, 'input', attrib={
            'type':'hidden',
            'name':'cell',
            'value':"{}_{}".format(r,c),
            })
        
        if c < len(row):
            if row[c]:
                #t.attrib["value"] = row[c].__unicode__()
                t.attrib["value"] = func(row[c], self)
            else:
                t.attrib["value"] = ""
        else:
            t.attrib["value"] = ""

        return td

    def html(self, func):

        table = et.Element('table')

        for row,r in zip(self.table, range(len(self.table))):
            
            tr = et.Element('tr')

            for c in range(np.shape(self.table)[1]):
                tr.append(self.html_col(row, r, c, func))
            
            table.append(tr)

        return et.tostring(table)



