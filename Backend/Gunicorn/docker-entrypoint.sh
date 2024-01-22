cd /app/backend

gunicorn backend.wsgi:application --bind
