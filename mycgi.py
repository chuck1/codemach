#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import cgitb
cgitb.enable()

import os
import sys
import cgi
import re
import array
import pickle
import xml.etree.ElementTree as et
import jinja2
import Cookie
import datetime
import random

import spreadsheet as ss
import spreadsheet.service

#with open("/var/www/html/cgi-bin/template.html", 'r') as f:
#    temp = jinja2.Template(f.read())

name_srv_w = "/tmp/python_spreadsheet_srv_w"
name_cli_w = "/tmp/python_spreadsheet_cli_w"

def detect_type(s):
    pat = '^\d+$'

    m = re.match(pat, s)

    return m

def read():
    with open(name_srv_w, 'rb') as f:
        return f.read()

def write(s):
    with open(name_cli_w, 'wb') as f:
        f.write(s)

def write_read(lst):
    for l in lst:
        write(l)
        read()

def get_sheet(username):
    req = ss.service.Request('get sheet', username)
    req.do()
    sheet = pickle.loads(req.res)
    return sheet

def form_sheet_ctrl():
    f = et.Element('form')
    i = et.SubElement(f, 'input', attrib={
        'type':'submit',
        'name':'btn add row',
        'value':'add row',
        })
    i = et.SubElement(f, 'input', attrib={
        'type':'submit',
        'name':'btn add col',
        'value':'add col',
        })
    i = et.SubElement(f, 'input', attrib={
        'type':'submit',
        'name':'btn show type',
        'value':'show type',
        })
    i = et.SubElement(f, 'input', attrib={
        'type':'submit',
        'name':'btn show',
        'value':'show',
        })
    i = et.SubElement(f, 'input', attrib={
        'type':'submit',
        'name':'btn logout',
        'value':'logout',
        })

    return f

def html_login(message, cookie_out, cookie_in):
    with open("/var/www/html/cgi-bin/template/login.html", 'r') as f:
        temp = jinja2.Template(f.read())

    return temp.render(
            message = message,
            cookie_out = cookie_out,
            cookie_in  = cookie_in,
            )

def html_sheet(username, cookie_out, cookie_in, display_func):
    with open("/var/www/html/cgi-bin/template.html", 'r') as f:
        temp = jinja2.Template(f.read())
    
    sheet = get_sheet(username)
    
    return temp.render(
        cookie_out = cookie_out,
        cookie_in  = cookie_in,
        html       = et.tostring(form_sheet_ctrl()) + sheet.html(display_func)
        )

def render_login(cookie_out, cookie_in, message):
    print "Content-Type: text/html"
    print cookie_out.output()
    print
    print html_login(message, cookie_out, cookie_in)

def render_sheet(username, cookie_out, cookie_in, display_func):
    print "Content-Type: text/html"
    print cookie_out.output()
    print
    print html_sheet(username, cookie_out, cookie_in, display_func)


def cookie_session(usr):
    expiration = datetime.datetime.now() + datetime.timedelta(minutes=30)
    cookie = Cookie.SimpleCookie()
    cookie["session"] = random.randint(0,1000000000)
    #cookie["session"]["domain"] = "127.0.0.1"
    cookie["session"]["domain"] = "67.160.178.216"
    cookie["session"]["path"] = "/"
    cookie["session"]["expires"] = expiration.strftime("%a, %d-%b-%Y %H:%M:%S PST")

    cookie["username"] = usr
    #cookie["username"]["domain"] = "127.0.0.1"
    cookie["username"]["domain"] = "67.160.178.216"
    cookie["username"]["path"] = "/"
    cookie["username"]["expires"] = expiration.strftime("%a, %d-%b-%Y %H:%M:%S PST")

    return cookie

###################################################3333

def gen(cookie_in):

    form = cgi.FieldStorage()
    keys = form.keys()
    #cookie_in = Cookie.SimpleCookie(os.environ.get("HTTP_COOKIE"))
    
    try:
        username = cookie_in["username"].value
    except:
        username = None
    
    ########################################################
    # checking how this page was called
    
    
    if 'btn add row' in keys:
        req = ss.service.Request('add row', username)
        req.do()
    
        render_sheet(
                username,
                Cookie.SimpleCookie(),
                cookie_in,
                lambda c,sheet: c.str_value(sheet)
                )
    
    elif 'btn add col' in keys:
        req = ss.service.Request('add col', username)
        req.do()
    
        render_sheet(
                username,
                Cookie.SimpleCookie(),
                cookie_in,
                lambda c,sheet: c.str_value(sheet)
                )
    
    elif 'btn show type' in keys:
        display_func = lambda c,sheet: c.str_type()
    
        render_sheet(
                username,
                Cookie.SimpleCookie(),
                cookie_in,
                lambda c,sheet: c.str_type()
                )
    
    elif ('cell' in keys) and ('text' in keys):
        req = ss.service.Request('set cell', username)
        req.cell = form['cell'].value
        req.text = form['text'].value
        req.do()
        
        render_sheet(
                username,
                Cookie.SimpleCookie(),
                cookie_in,
                lambda c,sheet: c.str_value(sheet)
                )
    
    elif 'btn_login' in keys:
        try:
            username = form['user'].value
            pwd = form['pass'].value
        except:
            renderer_login(
                    "must enter username and password",
                    Cookie.SimpleCookie(),
                    cookie_in
                    )
        else:
            req = ss.service.Request('login')
            req.u = username
            req.p = pwd
            req.do()
    
            if req.res == 'invalid pwd':
                render_login(
                        Cookie.SimpleCookie(),
                        cookie_in,
                        "invalid password")
            elif req.res == 'login success':
                render_sheet(
                username,
                        cookie_session(username),
                        cookie_in,
                        lambda c,sheet: c.str_value(sheet)
                        )
    
    elif 'btn logout' in keys:
        render_login(
            Cookie.SimpleCookie(),
            cookie_in,
            "logged out")
    
    else:
        try:
            ses = cookie_in["session"]
            #print "session = " + 
            pass
        except (Cookie.CookieError, KeyError):
            #print "session cookie not set!"
            
            render_login(
                    Cookie.SimpleCookie(),
                    cookie_in,
                    "session not set")
            
            pass
        else:
            render_sheet(
                    username,
                    Cookie.SimpleCookie(),
                    cookie_in,
                    lambda c,sheet: c.str_value(sheet)
                    )



