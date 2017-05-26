
bash test_sheets.bash

if [ $? -ne 0 ]
then
	exit 1
fi

python3 -m unittest sheets_backend.tests

if [ $? -ne 0 ]
then
	exit 1
fi


cd web_sheets_django

python3 manage.py test

cd ..

