FROM alpine:3.17

RUN apk update && apk upgrade && apk add python3 py3-pip

RUN pip3 install django

RUN pip3 install django-sslserver

COPY --chmod=777 docker-entrypoint.sh /docker-entrypoint.sh

RUN mkdir /app

WORKDIR /app

COPY --chmod=777 settings.py /app/settings.py

COPY --chmod=777 urls.py /app/urls.py

EXPOSE 8000

CMD ["/docker-entrypoint.sh"]
