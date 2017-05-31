
l='modconf codemach ws_storage ws_sheets ws_sheets_server'

for f in $l ;
do
	echo $f
	cat $f/VERSION.txt
	cd $f
	git branch
	cd ..
done



