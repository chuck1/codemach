#!/bin/bash

cd ..

bash check.bash

virtualenv venv

source venv/bin/activate

if [ $? -ne 0 ]
then
	exit 1
fi

pip3 install ./myexecutor_pkg
pip3 install ./mysocket_pkg
pip3 install ./storage_pkg
pip3 install ./sheets_pkg
pip3 install ./sheets_backend_pkg

mkdir -p venv/testing/log/web_sheets_sheets_backend

web_sheets_sheets_backend --settings ./testing &
pid=$!
echo $pid > pid.txt

cd web_sheets_django

python3 manage.py runserver 0.0.0.0:8006

kill $pid

