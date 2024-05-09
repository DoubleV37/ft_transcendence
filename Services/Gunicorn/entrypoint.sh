cd /app/Project

if [ ! -d "staticfiles" ]; then
	mkdir staticfiles
fi

python3 manage.py makemigrations

python3 manage.py migrate

python3 manage.py collectstatic --noinput

exec gunicorn Project.wsgi:application --bind 0.0.0.0:8000 --workers 3 --reload --log-level=debug
