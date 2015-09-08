#!/bin/bash


./setup.py install --force > /dev/null

cp python_spreadsheet.conf /etc/init/ -f

./deploy.bash


stop python_spreadsheet
start python_spreadsheet

