#!/bin/bash


celery -A celery_app worker -l info -Q bot


#celery multi start 2 -A celery_app -Q:1 q1 -Q:2 q2 -c:1 1 -c:2 1 -l info

