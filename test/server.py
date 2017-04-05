#!/usr/bin/env python3
import mysocket

server = mysocket.Server('', 6000)

server.main_loop()

