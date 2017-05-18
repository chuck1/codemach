
rm -rf venv

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

python3 -m unittest sheets_backend.tests.check_stored

#deactivate

