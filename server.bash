#!/bin/bash

./socket_server.py > log/server.log 2>&1 &

p=$!

echo $p > server_pid


