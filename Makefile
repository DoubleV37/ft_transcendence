all: up

up:
	if [ ! -d "Django_data/staticfiles" ]; then mkdir -p Django_data/staticfiles; fi
	docker compose up --build -d

down:
	docker compose down

stop:
	docker compose stop

fclean: down
	docker system prune -af --volumes
	docker volume rm `docker volume ls -q`

re: stop up

fre: fclean up

.PHONY: up down fclean re fre all stop
