
./increment_build_number.py

virtualenv venv

source venv/bin/activate

if [ $? -ne 0 ]
then
	exit 1
fi

pip3 install ./myexecutor_pkg
pip3 install ./sheets_pkg

python3 -m unittest sheets.tests.set_cell
python3 -m unittest sheets.tests.set_script_pre
python3 -m unittest sheets.tests.script_post
python3 -m unittest sheets.tests.security

