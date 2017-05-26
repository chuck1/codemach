
from web_sheets_django.settings.base import *

DEBUG = False

LOGGING['handlers']['file']['filename'] = '/var/log/web_sheets_django/debug.log'


