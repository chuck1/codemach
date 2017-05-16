from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.conf import settings
import django.contrib.auth

import json
import numpy
import logging

import sheets_backend.sockets

import sheets_app.models as models
import sheets_app.book_demos

logger = logging.getLogger(__name__)

# Create your views here.

def get_user_sheet_id(user, sheet_id):
    return str(user.id) + '_' + sheet_id

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
        v = c.value
        #if isinstance(v, str): v = "\"" + v + "\""
        return json.dumps([c.string, v])
    return numpy.vectorize(f, otypes=[str])(cells).tolist()

def index(request):
    if not request.user.is_authenticated():
        print('user not auth. redirect to login', repr(request.user))
        return HttpResponseRedirect(reverse('social:begin', args=['google-oauth2',])+'?next='+reverse('index'))

    user = django.contrib.auth.get_user(request)
    print('index')
    print('GET',list(request.GET.items()))

    if user.is_authenticated():
        books = list(user.book_user_creator.all())
    else:
        books = []
    
    context = {
            'user': user, 
            'books': books,
            'url_login_redirect': django.urls.reverse('index'),
            'url_logout_redirect': django.urls.reverse('index'),
            'url_select_account_redirect': django.urls.reverse('index'),
            }

    return render(request, 'sheets_app/index.html', context)

def book_demo(request, book_demo_name):
    
    func = sheets_app.book_demos.get_func(book_demo_name)

    book = book_new_func(book_demo_name)
    book.is_demo = True
    book.save()

    bp = sheets_backend.sockets.BookProxy(book.book_id, settings.WEB_SHEETS_PORT)

    func(bp)

    return redirect('sheets:book', book.id, 0)

def book(request, book_id, sheet_key):
   
    book = get_object_or_404(models.Book, pk=book_id)
    
    if not book.is_demo:
        if not request.user.is_authenticated():
            return HttpResponseRedirect(reverse('social:begin', args=['google-oauth2',])+'?next='+reverse('index'))
    
    user = django.contrib.auth.get_user(request)
    
    bp = sheets_backend.sockets.BookProxy(book.book_id, settings.WEB_SHEETS_PORT)
    
    ret = bp.get_sheet_data(sheet_key)
    
    print(ret)
    print(repr(ret.cells))
    
    cells = cells_array(ret)
    
    print('cells',repr(cells))
    
    context = {
        'cells': json.dumps(cells),
        'script_pre': ret.script_pre,
        'script_pre_output': ret.script_pre_output,
        'user': user,
        'book': book,
        'sheet_key': sheet_key,
        'url_login_redirect': django.urls.reverse('index'),
        'url_logout_redirect': django.urls.reverse('index'),
        'url_select_account_redirect': django.urls.reverse('index'),
        }
    return render(request, 'sheets_app/sheet.html', context)

def set_cell(request, book_id):
    sheet_key = request.POST["sheet_key"]
    r = int(request.POST['r'])
    c = int(request.POST['c'])
    s = request.POST['s']

    book = get_object_or_404(models.Book, pk=book_id)

    bp = sheets_backend.sockets.BookProxy(book.book_id, settings.WEB_SHEETS_PORT)

    ret = bp.set_cell(sheet_key, r, c, s)

    ret = bp.get_cell_data(sheet_key)
    
    cells = cells_array(ret)

    return JsonResponse({'cells':cells})

def get_sheet_data(request, book_id):
    sheet_key = request.POST["sheet_key"]
    
    book = get_object_or_404(models.Book, pk=book_id)
    
    bp = sheets_backend.sockets.BookProxy(book.book_id, settings.WEB_SHEETS_PORT)
 
    ret = bp.get_sheet_data(sheet_key)
    
    cells = cells_array(ret)

    logger.debug('sheet_data')
    logger.debug('script_pre_output')
    logger.debug(ret.script_pre_output)

    return JsonResponse({
        'cells': cells,
        'script_pre': ret.script_pre,
        'script_pre_output': ret.script_pre_output,
        'script_post': ret.script_post,
        'script_post_output': ret.script_post_output,
        })

def set_script_pre(request, book_id):
    sheet_key = request.POST["sheet_key"]
    s = request.POST['text']
    
    book = get_object_or_404(models.Book, pk=book_id)
    
    bp = sheets_backend.sockets.BookProxy(book.book_id, settings.WEB_SHEETS_PORT)
 
    ret = bp.set_script_pre(sheet_key, s)

    ret = bp.get_sheet_data(sheet_key)
    
    cells = cells_array(ret)

    print('set script pre')

    logger.debug('sheet_data')
    logger.debug('script_pre_output')
    logger.debug(ret.script_pre_output)

    return JsonResponse({
        'cells': cells,
        'script_pre': ret.script_pre,
        'script_pre_output': ret.script_pre_output,
        'script_post': ret.script_post,
        'script_post_output': ret.script_post_output,
        })

def alter_sheet(request, book_id, func):
    if not request.POST['i']:
        i = None
    else:
        i = int(request.POST['i'])
    
    sheet_key = request.POST["sheet_key"]
    
    book = get_object_or_404(models.Book, pk=book_id)
 
    bp = sheets_backend.sockets.BookProxy(book.book_id, settings.WEB_SHEETS_PORT)

    ret = func(bp, sheet_key, i)

    ret = bp.get_cell_data(sheet_key)
    
    cells = cells_array(ret)

    return JsonResponse({'cells':cells})

def add_column(request, book_id):
    return alter_sheet(request, book_id, sheets_backend.sockets.BookProxy.add_column)

def add_row(request, book_id):
    return alter_sheet(request, book_id, sheets_backend.sockets.BookProxy.add_row)

def book_new_func(book_name, user=None):
    
    c = sheets_backend.sockets.Client(settings.WEB_SHEETS_PORT)
    
    ret = c.book_new()

    print('new book id', repr(ret.book_id), type(ret.book_id))

    b = models.Book()
    b.user_creator = user
    b.book_id = ret.book_id
    b.book_name = book_name
    b.is_demo = False
    b.save()

    return b

@login_required
def book_new(request):
    book_name = request.POST['book_name']

    c = sheets_backend.sockets.Client(settings.WEB_SHEETS_PORT)
    
    ret = c.book_new()

    print('new book id', repr(ret.book_id), type(ret.book_id))

    b = models.Book()
    b.user_creator = request.user
    b.book_id = ret.book_id
    b.book_name = book_name
    b.is_demo = False
    b.save()

    return redirect('sheets:book', b.id, 0)



