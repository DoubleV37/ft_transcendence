cd /app/backend

django manage.py staticfiles --noinput

exec gunicorn backend.wsgi:application --bind 0.0.0.0:8000 --workers 3
