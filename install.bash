#!/bin/bash 

root=`pwd`


cd $root/mysocket
pip3 install -e .

cd $root/storage
pip3 install -e .

cd $root/sheets
pip3 install -e .

cd $root/sheets_backend
pip3 install -e .

cd $root

for f in daemon/*.conf; do
	ln -sf `pwd`/$f /etc/init/$(basename "$f" .conf).conf
done



