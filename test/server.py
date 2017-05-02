#!/usr/bin/env python3
import mysocket

class Foo(mysocket.ClientSocket):
    def __init__(self, sock):
        super(Foo, self).__init__(sock)

    def do_recv(self, b):
        print('data',repr(b))

        self.send('echo '.encode()+b)

server = mysocket.Server('', 6000, Foo)

server.run()

