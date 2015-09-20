#!/usr/bin/env python

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
import getpass

import python_spreadsheet as ss
import python_spreadsheet.service

def get_http_host():
    try:
        return os.environ['HTTP_HOST']
        #return "." + os.environ['HTTP_HOST']
        #return "http://" + os.environ['HTTP_HOST']
    except:
        return None

template_dir = "/usr/local/python_spreadsheet/templates/"

template_file_login = os.path.join(template_dir, "login.html")
template_file_sheet = os.path.join(template_dir, "sheet.html")

name_srv_w = "/tmp/python_spreadsheet_srv_w"
name_cli_w = "/tmp/python_spreadsheet_cli_w"

debug = False

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

def get_sheet(sessid):
    req = ss.service.Request('get sheet', sessid)
    req.do()
    
    if req.res[:5]=="error":
        raise ValueError(req.res)
    
    sheet = pickle.loads(req.res)
    return sheet

def form_sheet_ctrl(sessid):
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
        'name':'btn show raw',
        'value':'show raw',
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
    i = et.SubElement(f, 'input', attrib={
        'type':'hidden',
        'name':'sessid',
        'value':str(sessid),
        })

    return f



def debug_default(
        debug_lines,
        cookie_out,
        cookie_in):
    debug_lines.append(
            "cookie out  = {}".format(repr(str(cookie_out.output()))))
    debug_lines.append(
            "cookie in   = {}".format(repr(str(cookie_in.output()))))

def html_login(
        message, 
        cookie_out, 
        cookie_in, 
        debug_lines):

    with open(template_file_login, 'r') as f:
        temp = jinja2.Template(f.read())

    debug_default(
            debug_lines,
            cookie_out,
            cookie_in,
            )

    return temp.render(
            message     = message,
            debug_lines = "\n".join("<pre>"+l+"</pre>" for l in debug_lines),
            debug       = debug,
            )

def html_sheet(
        sessid,
        cookie_out, 
        cookie_in, 
        display_func, 
        debug_lines):

    with open(template_file_sheet, 'r') as f:
        temp = jinja2.Template(f.read())
    
    debug_default(
            debug_lines,
            cookie_out,
            cookie_in,
            )

    sheet = get_sheet(sessid)
    
    html  = et.tostring(form_sheet_ctrl(sessid))
    html += "\n"
    html += sheet.html(display_func, sessid)

    return temp.render(
        html            = html,
        debug_lines = "\n".join("<pre>"+l+"</pre>" for l in debug_lines),
        debug           = debug,
        )

def render_login(
        message, 
        cookie_out, 
        cookie_in, 
        debug_lines):
    #print cookie_out.output()
    #print cookie_out
    print "Content-Type: text/html"
    print cookie_out
    #print cookie_out.output()
    print
    print html_login(
            message,
            cookie_out, 
            cookie_in, 
            debug_lines)

def render_sheet(
        sessid, 
        cookie_out, 
        cookie_in, 
        display_func, 
        debug_lines):
    #print cookie_out.output()
    #print cookie_out
    print "Content-Type: text/html"
    print cookie_out
    #print cookie_out.output()
    print
    print html_sheet(
            sessid, 
            cookie_out, 
            cookie_in, 
            display_func, 
            debug_lines)

def cookie_item(cookie, expiration, k, v,):
    cookie[k] = v
    #cookie[k]["domain"] = get_http_host()
    cookie[k]["path"] = "/cgi/python_spreadsheet/"
    cookie[k]["expires"] = expiration.strftime("%a, %d-%b-%Y %H:%M:%S PST")

def cookie_session(usr, sess):
    expiration = datetime.datetime.now() + datetime.timedelta(minutes=30)
    cookie = Cookie.SimpleCookie()

    cookie_item(
            cookie,
            expiration,
            "session",
            sess,
            )

    cookie_item(
            cookie,
            expiration,
            "username",
            usr,
            )

    return cookie

######################################################

def gen(cookie_in):
    """
    main function called by cgi_script
    """
    form = cgi.FieldStorage()
    keys = form.keys()
    
    debug_lines = []

    try:
        username = cookie_in["username"].value
    except:
        username = None
    
    try:
        sessid = int(form["sessid"].value)
    except:
        sessid = None

    try:
        display = cookie_in["display"].value
    except:
        display = None
    
    if display:
        if display == 'type':
            display_func = lambda c,sheet,y,x: c.str_type()
        elif display == 'value':
            display_func = lambda c,sheet,y,x: c.str_value(sheet,y,x)
        elif display == 'raw':
            display_func = lambda c,sheet,y,x: c.str_raw()
        else:
            display_func = lambda c,sheet,y,x: c.str_value(sheet,y,x)
    else:
        display_func = lambda c,sheet,y,x: c.str_value(sheet,y,x)


    debug_lines.append(
            "username    = {}".format(repr(username)))
    debug_lines.append(
            "display     = {}".format(repr(display)))
    debug_lines.append(
            "domain      = {}".format(repr(get_http_host())))
    debug_lines.append(
            "cgi         = {}".format(repr(form)))
    
    for k,v in os.environ.items():
        debug_lines.append(
                "os.environ[{}] = {}".format(repr(k),repr(v)))

    debug_lines.append(
            "os.getuid   = {}".format(repr(os.getuid())))
    debug_lines.append(
            "getuser     = {}".format(repr(getpass.getuser())))
    debug_lines.append(
            "sessid      = {}".format(repr(sessid)))

    ########################################################

    # checking how this page was called
    
    cookie_out = Cookie.SimpleCookie()
    expiration = datetime.datetime.now() + datetime.timedelta(minutes=30)
   
    sheet_actions = [
            'btn add row',
            'btn add col',
            'btn show raw',
            'btn show type',
            'btn show']

    if set(sheet_actions).intersection(set(keys)):
        if 'btn add row' in keys:
            req = ss.service.Request('add row', sessid)
            req.do()
    
        elif 'btn add col' in keys:
            req = ss.service.Request('add col', sessid)
            req.do()
    
        elif 'btn show raw' in keys:
            display_func = lambda c,sheet,y,x: c.str_raw()

            cookie_item(cookie_out, expiration, "display", "raw")

        elif 'btn show' in keys:
            display_func = lambda c,sheet,y,x: c.str_value(sheet,y,x)

            cookie_item(cookie_out, expiration, "display", "value")

        elif 'btn show type' in keys:
            display_func = lambda c,sheet,y,x: c.str_type()

            cookie_item(cookie_out, expiration, "display", "type")
        else:
            raise ValueError()

        render_sheet(
                sessid,
                cookie_out,
                cookie_in,
                display_func,
                debug_lines,
                )

    
    elif ('cell' in keys) and ('text' in keys):
        req = ss.service.Request('set cell', sessid)
        req.cell = form['cell'].value
        req.text = form['text'].value
        req.do()

        debug_lines.append(
                "cell = {}".format(repr(req.cell)))
        debug_lines.append(
                "text = {}".format(repr(req.text)))

        render_sheet(
                sessid,
                cookie_out,
                cookie_in,
                display_func,
                debug_lines,
                )

    elif ('cell' in keys):
        debug_lines.append(
                "cell = {}".format(repr(form['cell'].value)))

        req = ss.service.Request('set cell', sessid)
        req.cell = form['cell'].value
        req.text = None
        req.do()

        render_sheet(
                sessid,
                Cookie.SimpleCookie(),
                cookie_in,
                display_func,
                debug_lines,
                )
    
    elif 'btn_login' in keys:
        try:
            username = form['user'].value
            pwd = form['pass'].value
        except:
            render_login(
                    "must enter username and password",
                    Cookie.SimpleCookie(),
                    cookie_in,
                    debug_lines,
                    )
        else:
            req = ss.service.Request('login')
            req.u = username
            req.p = pwd
            req.do()
    
            if req.res == 'invalid pwd':
                render_login(
                        "invalid password",
                        Cookie.SimpleCookie(),
                        cookie_in,
                        debug_lines,
                        )
            elif req.res[:13] == 'login success':
                sessid = int(req.res[14:])
                debug_lines.append(
                    "username    = {}".format(repr(username)))
                debug_lines.append(
                    "session     = {}".format(repr(sessid)))

                render_sheet(
                        sessid,
                        cookie_session(username, sessid),
                        cookie_in,
                        display_func,
                        debug_lines,
                        )
            else:
                raise ValueError(req.res)
    elif 'btn logout' in keys:
        render_login(
            "logged out",
            Cookie.SimpleCookie(),
            cookie_in,
            debug_lines,
            )
    else:
        if sessid:
            render_sheet(
                    sessid,
                    Cookie.SimpleCookie(),
                    cookie_in,
                    display_func,
                    debug_lines,
                    )
        else:
            render_login(
                    "session not set",
                    Cookie.SimpleCookie(),
                    cookie_in,
                    debug_lines,
                    )


