#!/usr/bin/env python3
import os
import jinja2
import aiohttp
import aiohttp.web
import sys
import json
import requests_oauthlib
import ssl
import modconf
import argparse
import pickle
import ws_sheets_server
import ws_sheets_server.packet

BASE_DIR = os.path.dirname(__file__)

SCHEME = 'http'
SCHEME_WS = 'ws'

class ClientProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        self.transport = transport
        print('client connection made')

    def data_received(self, data):
        print('Data received: {!r}'.format(data.decode()))

    def connection_lost(self, exc):
        print('The server closed the connection')

    def send_object(self, o):
        data = pickle.dumps(o)
        self.transport.write(data)

async def handler(request):

    print('host=',request.host)

    template = request.app['template_env'].get_template('sheet.html')
    
    text = template.render(
            ws_url=SCHEME_WS + '://' + request.host + '/ws')
    
    response = aiohttp.web.Response(body=text)
    response.content_type = 'text/html'
    return response

async def process_json_message(app, data):
    proto = app['client_proto']

    if data['type'] == 'get_sheet_data':
        proto.send_object(ws_sheets_server.packet.GetSheetData(0, 0))
        

async def handler_websocket(request):
    print('websocket handler')
    ws = aiohttp.web.WebSocketResponse()
    await ws.prepare(request)

    

    print('wait for message')
    async for msg in ws:
        print('msg', msg)
        if msg.type == aiohttp.WSMsgType.TEXT:
            if msg.data == 'close':
                await ws.close()
            else:
                print('msg text =', msg.data)

                try:
                    data = json.loads(msg.data)
                except:
                    pass
                else:
                    await process_json_message(data)

                #await ws.send_str(msg.data + '/answer')
        elif msg.type == aiohttp.WSMsgType.ERROR:
            print('ws connection closed with exception %s' %
                    ws.exception())

            print('websocket connection closed')

    return ws

async def handler_google_oauth2_login(request):
    
    scope = ['https://www.googleapis.com/auth/userinfo.email',
            'https://www.googleapis.com/auth/userinfo.profile']
    oauth = requests_oauthlib.OAuth2Session(
            conf.google_oauth2.client_id,
            redirect_uri=SCHEME + '://' + conf.google_oauth2.url + '/google_oauth2_response',
            scope=scope)

    authorization_url, state = oauth.authorization_url(
            'https://accounts.google.com/o/oauth2/auth',
            # access_type and approval_prompt are Google specific extra
            # parameters.
            access_type="offline", approval_prompt="force")

    print('state =',state)

    # Store the oauth object using state as identifier.
    # It will be needed in the response handler
    request.app['oauth'][state] = oauth
    
    return aiohttp.web.HTTPFound(authorization_url)

async def handler_google_oauth2_response(request):

    authorization_response = request.scheme + '://' + request.host + request.path_qs

    #state = request.match_info.get('state')

    state = request.GET['state']

    oauth = request.app['oauth'][state]

    token = oauth.fetch_token(
            'https://accounts.google.com/o/oauth2/token',
            authorization_response=authorization_response,
            # Google specific extra parameter used for client
            # authentication
            client_secret=conf.google_oauth2.client_secret)

    r = oauth.get('https://www.googleapis.com/oauth2/v1/userinfo')
    
    print(dict(r.json()))

    response = aiohttp.web.Response(text='hello')
    return response

async def on_startup(app):
    print('on startup')
    
    coro = app.loop.create_connection(
            partial(ClientProtocol),
            'localhost',
            app['conf'].ws_sheets_server.PORT)
    
    #client = app.loop.run_until_complete(coro)
    transport, proto = await coro

    print(proto)

    app['client_proto'] = proto

def main(argv):
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--conf_dir',
            nargs=1,
            default=(None,))
    parser.add_argument('conf_mod')
    args = parser.parse_args(argv[1:])

    app = aiohttp.web.Application()

    app['oauth'] = {}

    app['conf'] = modconf.import_conf(args.conf_mod)

    app['template_env'] = jinja2.Environment(
            loader=jinja2.PackageLoader('ws_web_aiohttp', 'templates'))

    app.router.add_get('/', handler)
    app.router.add_get('/ws', handler_websocket)
    
    app.router.add_get('/google_oauth2_login', handler_google_oauth2_login)
    app.router.add_get('/google_oauth2_response', handler_google_oauth2_response)
 
    static_dir = os.path.join(os.environ['HOME'], 'git/python_packages/web_sheets/handsontable/dist')
    print('static dir', static_dir)

    app.router.add_static('/static/handsontable',
            path=static_dir,
            name='static_hot')

    app.router.add_static('/static/',
            path=os.path.join(BASE_DIR, 'static'),
            name='static')

    if SCHEME=='https':
        ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS)
        ssl_context.load_cert_chain(
                app['conf'].certfile, 
                app['conf'].keyfile)
    
    #aiohttp.web.run_app(app, port=443, ssl_context=ssl_context)
    aiohttp.web.run_app(app)
    

if __name__ == '__main__':
    main(('','ws_web_aiohttp.tests.conf.simple'))
    
    

