#!/usr/bin/env python3
import os
import json
import sys
import logging

import sheets_backend.filesystem
import sheets_backend.sockets

logging.dictConfig({
	'version': 1,
	'disable_existing_loggers': False,
	'handlers': {
		'file': {
			'level': 'DEBUG',
			'class': 'logging.FileHandler',
			'filename':'/etc/web_sheets/log/books/debug.log'
			'formatter':'basic'
			},
		},
	'loggers': {
		'django': {
			'handlers': ['file'],
			'level': 'DEBUG',
			'propagate': True,
			},
		},
	'formatters': {
		"basic":{
			"format":"%(asctime)s %(module) %(levelname) %(message)"
			}
		}
	}

def test():

    secrets = json.loads(open("web_sheets_django/secrets.json", "r").read())

    folder = "/etc/web_sheets"
    port = secrets["port"]

    storage = sheets_backend.filesystem.Storage(folder)
    server = sheets_backend.sockets.Server(storage, port)
    server.run()

if __name__ == '__main__':
    try:
        test()
    except:
        logging.exception()
        raise

