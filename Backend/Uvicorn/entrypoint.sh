cd /app/backend

exec uvicorn backend.asgi:application --host 0.0.0.0 --port 8001 --workers 3
