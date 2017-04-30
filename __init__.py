#!/usr/bin/python
# This is a simple port-forward / proxy, written using only the default python
# library. If you want to make a suggestion or fix something you can contact-me
# at voorloop_at_gmail.com
# Distributed over IDC(I Don't Care) license
import socket
import select
import time
import sys

# Changing the buffer_size and delay, you can improve the speed and bandwidth.
# But when buffer get to high or delay go too down, you can broke things
buffer_size = 4096
delay = 0.0001

class Forward:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self, host, port):
        try:
            self.sock.connect((host, port))
            return self.sock
        except Exception as e:
            print(e)
            return False

class Comm(object):
    def write(self, b):
        self.sock.send(b)

class Client(Comm):
    def __init__(self, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))

    def recv(self):
        return self.sock.recv(10000)

class Server(Comm):

    def __init__(self, host, port, class_client):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((host, port))
        self.server.listen(200)

        self.class_client = class_client

        self.input_list = []

    def run(self):
        self.input_list.append(self.server)
        while 1:
            print('main loop')
            time.sleep(delay)
            ss = select.select
            inputready, outputready, exceptready = ss(self.input_list, [], [])
            for s in inputready:
                if s == self.server:
                    self.on_accept()
                    break

                b = s.recv(buffer_size)
                if len(b) == 0:
                    self.on_close(s)
                    break
                else:
                    #self.do_recv(s, b)
                    s.do_recv(b)

    def on_accept(self):
        clientsock, clientaddr = self.server.accept()
        
        print(clientaddr, "has connected")
        c = self.class_client(clientsock)
        self.input_list.append(c)

    def on_close(self, s):
        print(s.getpeername(), "has disconnected")
        #remove objects from input_list
        self.input_list.remove(s)

    """
    def do_recv(self, s, b):
        # here we can parse and/or modify the data before send forward
        print("bytes:",b)
    """



