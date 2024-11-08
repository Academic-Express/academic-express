#!/bin/bash -e

export DJANGO_SETTINGS_MODULE=app.settings_prod

python manage.py migrate
gunicorn -w4 -b 0.0.0.0:8000 --log-level=info app.wsgi:application
