#!/bin/sh

# Move Node Modules to static/
if [ "$HUEY" != 'True' ]; then
    NPS=/node_modules/*
    for n in $NPS
    do
        mv -v -n $n static/
    done
fi

# Check for DB Up
status=$(nc -z db 5432; echo $?)
while [ $status != 0 ]
do
  sleep 1s
  status=$(nc -z db 5432; echo $?)
done

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
        gunicorn dhs_site.wsgi -b 0.0.0.0:8000
    fi
fi
