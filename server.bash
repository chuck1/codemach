#!/bin/bash

p=`cat server_pid`

kill $p

./socket_server.py &

p=$!

echo $p > server_pid


