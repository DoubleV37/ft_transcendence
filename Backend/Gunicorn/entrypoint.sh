cd /app/backend

python3 manage.py collectstatic --noinput

exec gunicorn backend.wsgi:application --bind 0.0.0.0:8000 --workers 3
