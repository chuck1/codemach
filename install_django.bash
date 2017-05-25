

root=`pwd`

cp -f config/apache.conf /etc/apache2/apache2.conf

rsync -av web_sheets_django /var/www

cd web_sheets_django

python3 manage.py collectstatic --noinput

cd $root

