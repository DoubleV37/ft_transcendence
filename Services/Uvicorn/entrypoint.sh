cd /app/Project

exec uvicorn Project.asgi:application --host 0.0.0.0 --port 8001 --workers 4 --log-level debug --reload --forwarded-allow-ips='*' --proxy-headers 
```
