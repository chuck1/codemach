#!/bin/bash

# sheet_backend

service=web_sheets_sheets_backend.service

conf_dir=/etc/web_sheets_sheets_backend

log_dir=/var/log/web_sheets_sheets_backend

cp -f daemon/web_sheets_sheets_backend.service /lib/systemd/system

mkdir -p /etc/web_sheets_sheets_backend/web_sheets_sheets_backend
mkdir -p /etc/web_sheets_sheets_backend/storage

dst=/etc/web_sheets_sheets_backend/web_sheets_sheets_backend

cp -f daemon/web_sheets_sheets_backend/__init__.py $dst
cp -f daemon/web_sheets_sheets_backend/settings.py $dst

mkdir -p /var/log/web_sheets_sheets_backend

chown web_sheets:web_sheets /var/log/web_sheets_sheets_backend
chown web_sheets:web_sheets $conf_dir/storage


systemctl daemon-reload
systemctl $service restart
systemctl $service status


