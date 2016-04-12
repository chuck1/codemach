#!/bin/bash

#cgi_dir=$www/cgi-bin/python_spreadsheet

#dir=$www/projects/programming/python_spreadsheet

www=/var/www/html/python-spreadsheet

mkdir -p $www
mkdir -p $www/bin
mkdir -p $www/style

cp -f html/*.py $www/bin

cp -f html/style.css $www/style

#pydoc -w python_spreadsheet
#pydoc -w python_spreadsheet.sheet
#pydoc -w python_spreadsheet.mycgi
#pydoc -w python_spreadsheet.service
#pydoc -w python_spreadsheet.security

#mv *.html doc

#cp -rf doc $dir

