#!/bin/bash

www=/home/chuck/home/var/www/source
dir=$www/secret/cgi-bin/python_spreadsheet

mkdir -p $dir

cp -f html/* $dir

cp -f html/style.css $www/style/python_spreadsheet.css

#cd ~/git/www

#sudo ./copy.bash

