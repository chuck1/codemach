#!/bin/bash

service python_spreadsheet_service stop


./setup.py install --force

cp service.sh /etc/init.d/python_spreadsheet_service

cp python_spreadsheet.conf /etc/init/

./deploy.bash


service python_spreadsheet_service start

