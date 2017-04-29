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

import django

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

    def get_value(self, sheet, y, x):
        if self.dtype == 'formula':

            func_cell = lambda r,c: sheet.get_cell_value(r,c)
            func_row = lambda: y
            func_col = lambda: x
            
            global_objects = dict(sheet.global_objects)
            
            global_objects.update({
                    "cell": func_cell,
                    "row": func_row,
                    "col": func_col,
                    })
            
            try:
                ret = eval(self.v[1:], global_objects)
            except NameError as e:
                return e.message
            else:
                return ret
        else:
            return self.v
    
    def str_type(self):
        return str(self.dtype)
    
    def str_value(self, sheet, r, c):
        v = self.get_value(sheet, r, c)
        if v is not None:
            return str(v)
            #return repr(v)
        else:
            return ''
    
    def str_raw(self):
        return str(self.v)

def display_func_value(cell, sheet, y, x):
    return cell.str_value(sheet, y, x)
def display_func_formula(cell, sheet, y, x):
    return cell.str_raw()



class DisplayData(object):
    def __init__(self):
        self.display_func = display_func_value

class Sheet(object):
    def __init__(self):
        self.table = np.array([[Cell()]])
        #self.table = np.array([[Cell()]], dtype=Cell)
        
        self.display_data = DisplayData()

        self._builtins = {
                    'abs':      abs,
                    'all':      all,
                    'any':      any,
                    'range':    range,
                    'sum':      sum,
                    }

        self.global_objects = {
                    '__builtins__': self._builtins,
                    }

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
            #return self.table[c][r]
            return self.table[r,c]
        except:
            return "index error"

    def get_cell_value(self, r, c):
        if isinstance(r, int) and isinstance(c, int):
            try:
                ret = self.get_cell(r,c).get_value(self, r, c)
            except RuntimeError as e:
                ret = e.message

            return ret
        else:
            R,C = np.meshgrid(r,c,indexing='ij')
            cells = self.get_cells(R,C)

            print "get cell value"
            print "r", repr(r)
            print "c", repr(c)
            print "R", repr(R)
            print "C", repr(C)
            print "shape(cells)", np.shape(cells)

            #return str(np.shape(cells))

            return self.get_cell_value_1(cells, R, C)

    def get_cell_value_1(self, cells, R, C):
        
        #f = np.vectorize(lambda c: c.get_value(self, r, c), otypes=[np.float, np.int])
        #f = np.vectorize(lambda c: c.get_value(self, r, c))
        f = np.vectorize(lambda cell,r,c: cell.get_value(self, r, c), otypes=[object])
        
        #print "vectorize"
        #print cells
        
        """        
        values = [None]*len(cells)
       
        
        #return str(np.shape(R))+str(np.shape(C))+str(np.shape(cells))
    
        for cell,i,r,c in zip(cells, range(len(cells)), R, C):
            if isinstance(cell, Cell):
                values[i] = cell.get_value(self, r, c)
            else:
                values[i] = self.get_cell_value_1(cell, r, c)

        return values
        return str(cells)
        """
        try:
            a = f(cells,R,C)
            return a
        except TypeError:
            return "TypeError"
        except ValueError as e:
            return "ValueError:"+e.message

    def html_col(self, row, r, c, csrf_token):

        td = 0
        td = et.Element('td')
        
        form = et.SubElement(
                td, 
                'form', attrib={
                    'id':"form{}_{}".format(r,c),
                    "method": "post",
                    'class':'sheet',
                    })
 
        h = et.SubElement(form, 'input', attrib={
            'type': 'hidden',
            'name': "csrfmiddlewaretoken",
            'value': csrf_token,
            })
       
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
                t.attrib["value"] = self.display_data.display_func(row[c], self, r, c)
            else:
                t.attrib["value"] = ""
        else:
            t.attrib["value"] = ""

        return td

    def html(self, http_request):
        """
        func function used to render cell (value, formular, etc)
        """

        csrf_token = django.middleware.csrf.get_token(http_request)

        table = et.Element('table')
    
        # header
        tr = et.Element('tr')
        
        tr.append(et.Element('td'))
        
        for c in range(np.shape(self.table)[1]):
            th = et.Element('th')
            th.text = str(c)
            tr.append(th)
        
        table.append(tr)

        # body

        for row,r in zip(self.table, range(len(self.table))):
            
            tr = et.Element('tr')

            th = et.Element('th')
            th.text = str(r)
            tr.append(th)


            for c in range(np.shape(self.table)[1]):
                tr.append(self.html_col(row, r, c, csrf_token))
            
            table.append(tr)

        return et.tostring(table, method="html")





"""
    if display:
        if display == 'type':
            display_func = lambda c,sheet,y,x: c.str_type()
        elif display == 'value':
            display_func = lambda c,sheet,y,x: c.str_value(sheet,y,x)
        else:
            display_func = lambda c,sheet,y,x: c.str_value(sheet,y,x)
    else:
        display_func = lambda c,sheet,y,x: c.str_value(sheet,y,x)
"""












