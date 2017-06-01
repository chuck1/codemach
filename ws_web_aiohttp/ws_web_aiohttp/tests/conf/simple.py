import os
import modconf

url = 'www.charlesrymal.com'

certfile = '/etc/letsencrypt/live/www.charlesrymal.com/fullchain.pem'
keyfile = '/etc/letsencrypt/live/www.charlesrymal.com/privkey.pem'

google_oauth2 = modconf.import_conf('google_oauth2', os.path.join(os.environ['HOME'], 'config'))

ws_sheets_server = modconf.import_conf('ws_sheets_server.tests.conf.simple')


