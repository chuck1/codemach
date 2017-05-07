from django.shortcuts import render
from django.http import JsonResponse

import django.contrib.auth

import json
import numpy

import sheets_backend.sockets

# Create your views here.


def mypipeline(backend, strategy, details, response, user=None, *args, **kwargs):
    print('mypipline')
    print('backend ',backend)
    print('strategy',strategy)
    print('details ',details)
    print('response',response)
    print('user    ',user)

    user.profile_image_url = response['image'].get('url')
    user.save()

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
    user = django.contrib.auth.get_user(request)
    print('index')
    print('user is auth', user.is_authenticated())

    if user.is_authenticated():
        sheet_ids = [sheet.sheet_id for sheet in user.sheet_user_creator.all()]
    else:
        sheet_ids = []
    
    context = {'user': user, 'sheet_ids': sheet_ids}
    return render(request, 'sheets_app/index.html', context)

def sheet(request, sheet_id):
    u = django.contrib.auth.get_user(request)
    print('user',repr(u))
    for k, v in u.__dict__.items():
        print('  ', k, v)

    sp = sheets_backend.sockets.SheetProxy(sheet_id)
    
    ret = sp.get_sheet_data()

    print(ret)
    print(repr(ret.cells))

    cells = cells_array(ret)
    
    print('cells',repr(cells))
    
    context = {
        'cells': json.dumps(cells),
        'script': ret.script,
        'script_output': ret.script_output,
        'user': u,
        'sheet_id': sheet_id
        }
    return render(request, 'sheets_app/sheet.html', context)

def set_cell(request, sheet_id):
    r = int(request.GET['r'])
    c = int(request.GET['c'])
    s = request.GET['s']
 
    sp = sheets_backend.sockets.SheetProxy(sheet_id)

    ret = sp.set_cell(r, c, s)

    ret = sp.get_cell_data()
    
    cells = cells_array(ret)

    return JsonResponse({'cells':cells})

def set_exec(request, sheet_id):
    print('set script')
    print('post')
    for k, v in request.POST.items(): print('  ',k,v)
    s = request.POST['text']
    print('set exec')
    print(repr(s))
    sp = sheets_backend.sockets.SheetProxy(sheet_id)

    ret = sp.set_exec(s)

    ret = sp.get_sheet_data()
    
    cells = cells_array(ret)

    return JsonResponse({'cells':cells, 'script':ret.script, 
            'script_output':ret.script_output,})

def add_column(request, sheet_id):
    if not request.GET['i']:
        i = None
    else:
        i = int(request.GET['i'])

    sp = sheets_backend.sockets.SheetProxy(sheet_id)

    ret = sp.add_column(i)

    ret = sp.get_cell_data()
    
    cells = cells_array(ret)

    return JsonResponse({'cells':cells})


