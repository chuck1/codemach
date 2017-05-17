#!/bin/bash 

root=`pwd`

pip3 install .

systemctl daemon-reload

for f in daemon/*.service; do
	src=$root/$f
	name=$(basename "$f" .service)
	dst=/lib/systemd/system/$(basename "$f" .service).service
	echo $src
	echo $dst
	echo $name

	mkdir -p /var/log/$name

done

chown web_sheets:web_sheets /var/log/web_sheets_sheets_backend
mkdir /etc/web_sheets_sheets_backend/storage
chown web_sheets:web_sheets /etc/web_sheets_sheets_backend/storage

for f in daemon/*.service; do
	name=$(basename "$f" .service)
	systemctl restart $name
	systemctl status $name
done

