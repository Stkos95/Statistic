#!/bin/bash


python manage.py collectstatic

gunicorn --bind :8000 todo.wsgi:application

