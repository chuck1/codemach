from django.shortcuts import render

import json
import numpy

import sheets_backend.sockets

# Create your views here.

def cells_values(cells):
    def f(c):
        return c.value
    return numpy.vectorize(f, otypes=[str])(cells)

def index(request):

    sp = sheets_backend.sockets.SheetProxy('0')
    ret = sp.get_cell_data()
    print(ret)
    print(repr(ret.cells))

    values = cells_values(ret.cells)
    
    print(repr(values))
    
    print(numpy.shape(values))

    context = {'cells':json.dumps(values.tolist())}
    return render(request, 'sheets_app/index.html', context)

