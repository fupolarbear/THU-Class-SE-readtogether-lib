#!/bin/sh
mysql -u root -p -e 'DROP DATABASE ReadTogether;'
mysql -u root -p -e 'CREATE DATABASE ReadTogether CHARACTER SET utf8;'
python manage.py syncdb
python manage.py loaddata initdata.json
