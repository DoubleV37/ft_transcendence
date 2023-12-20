FROM alpine:3.17

RUN apk update && apk upgrade && apk add python3 py3-pip tzdata libpq

COPY --chmod=777 requirements.txt /requirements.txt

RUN pip3 install -r requirements.txt

COPY --chmod=777 docker-entrypoint.sh /docker-entrypoint.sh

RUN mkdir /app

WORKDIR /app

RUN mkdir /app/backend

EXPOSE 8000

CMD ["/docker-entrypoint.sh"]
