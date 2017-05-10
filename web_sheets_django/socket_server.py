#!/usr/bin/env python3
import os
import sys

import sheets_backend.filesystem
import sheets_backend.sockets

def test():
    folder = '/home/chuck/sheets'
    port = 10001

    storage = sheets_backend.filesystem.Storage(folder)
    server = sheets_backend.sockets.Server(storage, port)
    server.run()

if __name__ == '__main__':
    test()

