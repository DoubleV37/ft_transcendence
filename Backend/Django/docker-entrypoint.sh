#!/bin/sh

django-admin startproject backend

cd /app/backend

mv /app/settings.py /app/backend/backend/settings.py
mv /app/urls.py /app/backend/backend/urls.py
mv /app/views.py /app/backend/backend/views.py
mv /app/manage.py /app/backend/manage.py
mv /app/templates /app/backend/templates

exec python3 manage.py runsslserver 0.0.0.0:8000
