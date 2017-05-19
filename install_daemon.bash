
# storage

cp -f daemon/web_sheets_storage.service /lib/systemd/system

mkdir -p /etc/web_sheets_storage/web_sheets_storage

cp -f daemon/web_sheets_storage/__init__.py /etc/web_sheets_storage/web_sheets_storage
cp -f daemon/web_sheets_storage/settings.py /etc/web_sheets_storage/web_sheets_storage

mkdir -p /var/log/web_sheets_storage

# sheet_backend

cp -f daemon/web_sheets_sheets_backend.service /lib/systemd/system

mkdir -p /etc/web_sheets_sheets_backend/web_sheets_sheets_backend
mkdir -p /etc/web_sheets_sheets_backend/storage

dst=/etc/web_sheets_sheets_backend/web_sheets_sheets_backend

cp -f daemon/web_sheets_sheets_backend/__init__.py $dst
cp -f daemon/web_sheets_sheets_backend/settings.py $dst

mkdir -p /var/log/web_sheets_sheets_backend

chown web_sheets:web_sheets /var/log/web_sheets_sheets_backend
chown web_sheets:web_sheets /etc/web_sheets_sheets_backend/storage

# start daemons

systemctl daemon-reload

for f in daemon/*.service; do
	name=$(basename "$f" .service)
	systemctl restart $name
	systemctl status $name
done


