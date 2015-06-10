#!/bin/bash

cp cgi_script.py ~/git/www/html/cgi-bin/cgi_spreadsheet.py -f

cp -rf template ~/git/www/html/cgi-bin/

cd ~/git/www

sudo ./copy.bash

