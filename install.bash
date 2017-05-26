#!/bin/bash 

root=`pwd`

echo version=\'`cat VERSION.txt`\' > sheets_pkg/sheets/version.py

pip3 install ./myexecutor_pkg
pip3 install ./mysocket_pkg
pip3 install ./storage_pkg
pip3 install ./sheets_pkg
pip3 install ./sheets_backend_pkg

./install_django.bash

# todo
# create user web_sheets if not exists
# for hot: npm install, grunt --force

./install_daemon.bash

systemctl restart apache2.service

