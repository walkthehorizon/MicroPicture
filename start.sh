#!/bin/bash
python manage.py collectstatic --noinput&&uwsgi --ini ./uwsgi.ini&&tail -f /dev/null