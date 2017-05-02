#!/usr/bin/env python3

import sheets_backend.filesystem
import sheets_backend.sockets

def test():
    storage = sheets_backend.filesystem.Storage()
    server = sheets_backend.sockets.Server(storage)
    server.run()

if __name__ == '__main__':
    test()

