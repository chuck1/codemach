
from web_sheets_django.settings.base import *

DEBUG = True

# production environment does not have HOME env var
STATICFILES_DIRS = [
        os.path.join(BASE_DIR, "static"),
        os.path.join(BASE_DIR, '../handsontable/dist'),
        os.path.join(os.environ['HOME'], 'static'),]

WEB_SHEETS_PORT = secrets['port_testing']

