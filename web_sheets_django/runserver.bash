#!/bin/bash

cd ..

web_sheets_sheets_backend --settings ./testing &
pid=$!
echo $pid > pid.txt

cd web_sheets_django

python3 manage.py runserver 0.0.0.0:8006

kill $pid

