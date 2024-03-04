#!/bin/sh

docker exec gunicorn python manage.py makemigrations
docker exec gunicorn python manage.py migrate
