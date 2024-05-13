all: up

env:
	@if [ ! -f "$(HOME)/.env" ]; then \
		echo "Please create a.env file in your home directory" && exit 1 ; \
	else \
		echo "Copying .env file from $(HOME)/.env" ; \
		cp $(HOME)/.env . ; \
		sed -i -e "s/target/$(shell hostname -i)/g" .env ; \
	fi

up: env
	if [ ! -d "Django_data/staticfiles" ]; then mkdir -p Django_data/staticfiles; fi
	docker compose up --build -d

elkup:
	docker compose up setup es01 logstash_nginx logstash_gunicorn rsyslog kibana --build -d

elkdown:
	docker compose down setup es01 logstash_nginx logstash_gunicorn rsyslog kibana

elkclean: elkdown
	docker system prune -af --volumes
	docker volume rm certs esdata01 kibanadata logstashdata01 logstashdata02

elkfre: elkclean elkup

down:
	docker compose down

stop:
	docker compose stop

fclean: down update
	docker system prune -af --volumes
	docker volume rm `docker volume ls -q`


re: stop up

fre: fclean up

site: env
	docker compose restart gunicorn
	docker compose restart uvicorn
	docker compose restart pong

update:
	rm -rf `find ./Django_data/ -type f -name "0*"`

.PHONY: up down fclean re fre all stop site update elkup elkdown elkclean elkfre env
