#!/bin/sh

cd /app/backend

exec python3 manage.py runsslserver 0.0.0.0:8000
