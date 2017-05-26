
mkdir /var/log/web_sheets_django -p

chown -R www-data:www-data /var/log/web_sheets_django


root=`pwd`

cp -f config/web_sheets.conf /etc/apache2/sites-available
a2ensite web_sheets.conf


rsync -av web_sheets_django /var/www

#cd web_sheets_django
#python3 manage.py collectstatic --noinput
#cd $root

chown -R www-data:www-data /var/www/web_sheets_django



