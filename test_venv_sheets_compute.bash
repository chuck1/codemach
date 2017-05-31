
make

if [ $? -ne 0 ]
then
	exit 1
fi

source venv/bin/activate

#bash test_sheets.bash

python3 -m unittest ws_sheets_server.tests -v

