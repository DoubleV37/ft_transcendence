all: up

up:
	docker compose up --build

down:
	docker compose down

stop:
	docker compose stop

fclean: down
	docker system prune -af --volumes

re: stop up

fre: fclean up

.PHONY: up down fclean re fre all stop
