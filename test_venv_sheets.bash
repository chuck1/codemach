
make

virtualenv venv

source venv/bin/activate

if [ $? -ne 0 ]
then
	exit 1
fi

pip3 install --find-links=package_index -U ws_sheets

bash test_sheets.bash

