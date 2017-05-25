
./increment_build_number.py

virtualenv venv

source venv/bin/activate

if [ $? -ne 0 ]
then
	exit 1
fi

pip3 install ./mysocket_pkg
pip3 install ./storage_pkg
pip3 install ./sheets_pkg
pip3 install ./sheets_backend_pkg

#pip3 install . -v

mkdir -p venv/testing/log/web_sheets_sheets_backend

which web_sheets_sheets_backend

web_sheets_sheets_backend --settings ./testing &
pid=$!
echo $pid > pid.txt

bash test.bash

kill `cat pid.txt`

#deactivate

