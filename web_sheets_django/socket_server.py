#!/usr/bin/env python3
import os
import sys

import sheets_backend.filesystem
import sheets_backend.sockets

def test():
    folder = sys.argv[1]
    port = int(sys.argv[2])

    storage = sheets_backend.filesystem.Storage(folder)
    server = sheets_backend.sockets.Server(storage, port)
    server.run()

if __name__ == '__main__':
    test()

