#!/bin/sh
mysql -u root -e 'DROP DATABASE IF EXISTS ReadTogether;'
mysql -u root -e 'CREATE DATABASE ReadTogether CHARACTER SET utf8;'
python manage.py syncdb --noinput
