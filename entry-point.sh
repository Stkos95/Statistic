#!/bin/bash


python manage.py collectstatic
python manage.py migrate
python manage.py loaddata --exclude auth.permission --exclude contenttypes dump/work_dump.json


gunicorn --bind :8000 todo.wsgi:application

