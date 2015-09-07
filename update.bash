#!/bin/bash

stop python_spreadsheet


./setup.py install --force

cp python_spreadsheet.conf /etc/init/

./deploy.bash


start python_spreadsheet

