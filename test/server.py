#!/usr/bin/env python3
import mysocket

class Foo(object):
    def __init__(self,sock):
        self.sock=sock
    def do_recv(self,b):
        print('data',repr(b))
    def fileno(self):
        return self.sock.fileno()
    def recv(self,buffer_size):
        return self.sock.recv(buffer_size)

server = mysocket.Server('', 6000, Foo)

server.run()

