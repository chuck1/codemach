#!/usr/bin/env python3
import mysocket
import struct

client = mysocket.Client('', 6000)

client.sock.send(struct.pack('I',255))

print(client.recv())



