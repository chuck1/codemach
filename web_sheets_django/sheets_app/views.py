from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.conf import settings
import django.contrib.auth
import django.views

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

def login_redirect(url_next):
    return HttpResponseRedirect(
            reverse('social:begin', args=['google-oauth2',])+'?next='+url_next)

def check_permission(request, book):
        if not book.is_demo:
            if not request.user.is_authenticated():
                return login_redirect(reverse('index'))
        
            if not (request.user == book.user_creator):
                return HttpResponseForbidden("You shall not pass.")
    

def index(request, messages=[]):
    if not request.user.is_authenticated():
        return login_redirect(reverse('index'))

    user = django.contrib.auth.get_user(request)
    
    logger.debug('index')
    logger.debug('GET',list(request.GET.items()))

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
            'messages': messages
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

class SimpleMessage(object):
    def __init__(self, msgtype, msg):
        self.msgtype = msgtype
        self.msg = msg

class BookView(django.views.View):

    def post(self, request, book_id):
        return self.do_view(request, book_id, self.post_sub)

    def get(self, request, book_id):
        return self.do_view(request, book_id, self.get_sub)

    def do_view(self, request, book_id, sub_function):

        book = get_object_or_404(models.Book, pk=book_id)

        if not book.is_demo:
            if not request.user.is_authenticated():
                return login_redirect(reverse('index'))
        
            if not (request.user == book.user_creator):
                return HttpResponseForbidden("You shall not pass.")

        bp = sheets_backend.sockets.BookProxy(book.book_id, settings.WEB_SHEETS_PORT)
            
        return sub_function(request, book, bp)


class BookViewView(BookView):
    def get_sub(self, request, book, bp):
       
        user = django.contrib.auth.get_user(request)
        
        sheet_key = '0'

        ret = bp.get_sheet_data(sheet_key)
        
        print(ret)
        print(repr(ret.cells))
        
        cells = cells_array(ret)
        
        print('cells',repr(cells))
        
        context = {
            'cells': json.dumps(cells),
            'script_pre': ret.script_pre,
            'script_pre_output': ret.script_pre_output,
            'script_post': ret.script_post,
            'script_post_output': ret.script_post_output,
            'user': user,
            'book': book,
            'sheet_key': sheet_key,
            'url_login_redirect': django.urls.reverse('index'),
            'url_logout_redirect': django.urls.reverse('index'),
            'url_select_account_redirect': django.urls.reverse('index'),
            }

        return render(request, 'sheets_app/sheet.html', context)

class SetCellView(BookView):
    def post_sub(self, request, book, bp):
    
        sheet_key = request.POST["sheet_key"]
        r = int(request.POST['r'])
        c = int(request.POST['c'])
        s = request.POST['s']
    
        ret = bp.set_cell(sheet_key, r, c, s)
    
        ret = bp.get_cell_data(sheet_key)
        
        cells = cells_array(ret)
    
        return JsonResponse({'cells':cells})

class ExceptionWithResponse(Exception):
    def __init__(self, response):
        super(ExceptionWithResponse, self).__init__(str(self))
        self.response = response

def sheet_data_response(bp, sheet_key):
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

class GetSheetDataView(BookView):
    def post_sub(self, request, book, bp):
        
        sheet_key = request.POST["sheet_key"]
        
        return sheet_data_response(bp, sheet_key)

class SetScriptPreView(BookView):
    def post_sub(self, request, book, bp):
        sheet_key = request.POST["sheet_key"]
        s = request.POST['text']
        
        ret = bp.set_script_pre(s)
    
        return sheet_data_response(bp, sheet_key)

class SetScriptPostView(BookView):
    def post_sub(self, request, book, bp):
        sheet_key = request.POST["sheet_key"]
        s = request.POST['text']
        
        ret = bp.set_script_post(s)
        
        ret = bp.get_script_post_output()

        return JsonResponse({'script_post_output': ret.script_post_output})

class AlterSheetView(BookView):
    def post_sub(self, request, book, bp):
        if not request.POST['i']:
            i = None
        else:
            i = int(request.POST['i'])
        
        sheet_key = request.POST["sheet_key"]
        
        ret = self.func(bp, sheet_key, i)
    
        ret = bp.get_cell_data(sheet_key)
        
        cells = cells_array(ret)
    
        return JsonResponse({'cells':cells})

class AddColumnView(AlterSheetView):
    func = staticmethod(sheets_backend.sockets.BookProxy.add_column)

class AddRowView(AlterSheetView):
    func = staticmethod(sheets_backend.sockets.BookProxy.add_row)

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

    b = book_new_func(book_name, request.user)

    return redirect('sheets:book', b.id)



