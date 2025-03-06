#!/bin/sh
if [ "$HUEY" == 'True' ]; then
    python manage.py run_huey
else
    python manage.py makemigrations --noinput
    python manage.py migrate --noinput
    python manage.py collectstatic --noinput 1> /dev/null

    # check if $CERT_FULLCHAIN_PATH and $CERT_KEY_PATH are set
    GUNICORN_CMD_ARGS = ""
    if [ "$CERT_FULLCHAIN_PATH" ] && [ "$CERT_KEY_PATH" ]; then
        echo "CERT_FULLCHAIN_PATH and CERT_KEY_PATH are set, setting up SSL"

        GUNICORN_CMD_ARGS = "--certfile=$CERT_FULLCHAIN_PATH --keyfile=$CERT_KEY_PATH"

        # in case lets encrypt is used, we need to wait for the certs to be generated
        while [ ! -f $CERT_FULLCHAIN_PATH ] || [ ! -f $CERT_KEY_PATH ]; do
            echo "Waiting for certs to be generated..."
            sleep 2
        done
    fi

    if [ "$DEBUG" == 'True' ]; then
        echo "DEBUG mode enabled"
        python manage.py runserver 0.0.0.0:8000
    else
        gunicorn radius_admin.wsgi -b 0.0.0.0:8000 $GUNICORN_CMD_ARGS
    fi
fi
