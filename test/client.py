#!/usr/bin/env python3
import mysocket

client = mysocket.Client('', 6000)

client.write('hello'.encode('utf-8'))

