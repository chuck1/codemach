
from web_sheets_django.settings.base import *

DEBUG = True

STATICFILES_DIRS = [
        os.path.join(BASE_DIR, "static"),
        os.path.join(os.environ['HOME'], 'git/handsontable/dist'),
        os.path.join(os.environ['HOME'], 'static'),]

