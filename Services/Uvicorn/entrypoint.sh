cd /app/Project

exec uvicorn Project.asgi:application --host 0.0.0.0 --port 8001 --workers 3
