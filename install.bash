#!/bin/bash 

cd ..

cd mysocket
pip3 install -e .
cd ..

cd storage
pip3 install -e .
cd ..

cd sheets
pip3 install -e .
cd ..

cd sheets_backend
pip3 install -e .
cd ..

cd web_sheets

for f in daemon/*.conf; do
	ln -sf `pwd`/$f /etc/init/$(basename "$f" .conf).conf
done

#ln -s daemon/web_sheets_storage.conf /etc/init/web_sheets_storage.conf
#ln -s daemon/web_sheets_storage.conf /etc/init/web_sheets_storage.conf


