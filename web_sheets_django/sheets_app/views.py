from django.shortcuts import render
from django.http import JsonResponse

import json
import numpy

import sheets_backend.sockets

# Create your views here.

def cells_values(ret):
    cells = ret.cells
    def f(c):
        return c.value
    return numpy.vectorize(f, otypes=[str])(cells).tolist()

def index(request):

    sp = sheets_backend.sockets.SheetProxy('0')
    ret = sp.get_cell_data()
    print(ret)
    print(repr(ret.cells))

    values = cells_values(ret)
    
    print(repr(values))
    
    print(numpy.shape(values))

    context = {'cells':json.dumps(values)}
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
    
    values = cells_values(ret)
    
    print(values)

    return JsonResponse({'cells':values})

