# Environment Requirements

- Git 1.7.9.5
- Python 2.7.3
- Django 1.6
- MySQL 5.5.34
- MySQLdb 1.2.4

## Sample Install Commands on Ubuntu 12.04

    sudo apt-get install mysql-server libmysqlclient-dev python-dev # mysql-password: 'root'
    echo -e "[client]\npassword=root" > ~/.my.cnf
    sudo pip install Django==1.6
    sudo pip install MySQL-python==1.2.4
    sudo pip install pytz==2013.8
    mysql_tzinfo_to_sql /usr/share/zoneinfo | mysql -u root mysql

# Install ReadTogether

    ./rebuildDB.sh
    export PYTHONPATH=$PYTHONPATH:/path/to/this/file/
    export DJANGO_SETTINGS_MODULE=thesite.settings

## Run It

    python manage.py runserver

## Crontab

    python -c 'from rt.models import Rank; Rank.update();'           # weekly or monthly
    python -c 'from rt.models import Borrowing; Borrowing.notify();' # daily

