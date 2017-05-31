
make

if [ $? -ne 0 ]
then
	exit 1
fi

virtualenv venv

source venv/bin/activate

if [ $? -ne 0 ]
then
	exit 1
fi

pip3 install -U --find-links=package_index sheets_backend

#bash test_sheets.bash

python3 -m unittest sheets_backend.tests -v

