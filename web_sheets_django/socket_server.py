#!/usr/bin/env python3
import os
import json
import sys

import sheets_backend.filesystem
import sheets_backend.sockets

def test():

    secrets = json.loads(open("secrets.json", "r").read())

    folder = "/etc/web_sheets"
    port = secrets["port"]

    storage = sheets_backend.filesystem.Storage(folder)
    server = sheets_backend.sockets.Server(storage, port)
    server.run()

if __name__ == '__main__':
    test()

