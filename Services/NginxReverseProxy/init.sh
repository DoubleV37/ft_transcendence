#!/bin/sh

openssl req -x509 -nodes -out /etc/nginx/ssl/transcendence.crt \
	-keyout /etc/nginx/ssl/transcendence.key \
	-subj "/C=FR/ST=Nouvelle-Aquitaine/L=Angouleme/O=42/OU=42/CN=*"

nginx -g "daemon off;"
