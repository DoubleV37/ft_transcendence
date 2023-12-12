#!/bin/sh

django-admin startproject backend

cd /app/backend

exec python3 manage.py runserver 0.0.0.0:8000
