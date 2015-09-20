#!/bin/bash

www=/home/chuck/home/var/www/source
cgi_dir=$www/cgi-bin/python_spreadsheet
dir=$www/projects/programming/python_spreadsheet

mkdir -p $dir

cp -f html/*.py $cgi_dir

cp -f html/style.css $www/style/python_spreadsheet.css

pydoc -w python_spreadsheet
pydoc -w python_spreadsheet.sheet
pydoc -w python_spreadsheet.mycgi
pydoc -w python_spreadsheet.service
pydoc -w python_spreadsheet.security

mv *.html doc

cp -rf doc $dir

