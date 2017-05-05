from django.shortcuts import render
from django.http import JsonResponse

import django.contrib.auth

import json
import numpy

import sheets_backend.sockets

# Create your views here.

def cells_values(ret):
    cells = ret.cells
    def f(c):
        return c.value
    return numpy.vectorize(f, otypes=[str])(cells).tolist()

def cells_array(ret):
    cells = ret.cells
    def f(c):
        return json.dumps([c.string, c.value])
    return numpy.vectorize(f, otypes=[str])(cells).tolist()

def index(request):
    u = django.contrib.auth.get_user(request)
    print('user',repr(u))
    print(u.__dict__)

    sp = sheets_backend.sockets.SheetProxy('0')
    ret = sp.get_cell_data()
    print(ret)
    print(repr(ret.cells))

    cells = cells_values(ret)
    cells = cells_array(ret)
    
    print('cells',repr(cells))
    
    context = {'cells':json.dumps(cells)}
    return render(request, 'sheets_app/index.html', context)

def set_cell(request):
    r = int(request.GET['r'])
    c = int(request.GET['c'])
    s = request.GET['s']
 
    print('set_cell')
    print(repr(r),repr(c),repr(s))
   
    sp = sheets_backend.sockets.SheetProxy('0')

    ret = sp.set_cell(r, c, s)

    ret = sp.get_cell_data()

    print('ret',ret)
    
    cells = cells_values(ret)
    cells = cells_array(ret)
    
    print('cells',cells)

    return JsonResponse({'cells':cells})

def add_column(request):
    if not request.GET['i']:
        i = None
    else:
        i = int(request.GET['i'])

    sp = sheets_backend.sockets.SheetProxy('0')

    ret = sp.add_column(i)

    ret = sp.get_cell_data()
    
    cells = cells_array(ret)

    return JsonResponse({'cells':cells})


