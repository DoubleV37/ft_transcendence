FROM nginx:1.25-alpine

COPY --chmod=655 init.sh /
COPY --chmod=777 nginx.conf /etc/nginx/nginx.conf

RUN	apk update && apk upgrade && apk add openssl; \
	mkdir -p /etc/nginx/ssl/

EXPOSE 8080

CMD [ "sh", "init.sh" ]
