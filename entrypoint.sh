#!/bin/sh
if [ "$HUEY" == 'True' ]; then
    python manage.py run_huey
else
    python manage.py makemigrations --noinput
    python manage.py migrate --noinput
    python manage.py collectstatic --noinput 1> /dev/null
    if [ "$DEBUG" == 'True' ]; then
        echo "DEBUG mode enabled"
        python manage.py runserver 0.0.0.0:8000
    else
        gunicorn radius_admin.wsgi -b 0.0.0.0:8000
    fi
fi
