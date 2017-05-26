
./increment_build_number.py

virtualenv venv

source venv/bin/activate

if [ $? -ne 0 ]
then
	exit 1
fi

pip3 install ./myexecutor_pkg
pip3 install ./sheets_pkg

bash test_sheets.bash

