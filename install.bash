#!/bin/bash 

root=`pwd`

echo version=\'`cat VERSION.txt`\' > sheets_pkg/sheets/version.py

pip3 install .

# todo
# create user web_sheets if not exists
# for hot: npm install, grunt --force

./install_daemon.bash

systemctl restart apache2.service

