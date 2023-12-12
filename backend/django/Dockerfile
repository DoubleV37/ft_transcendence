FROM alpine:3.17

RUN apk update && apk upgrade && apk add python3 py3-pip

RUN pip3 install django

COPY --chmod=777 entrypoint.sh /entrypoint.sh

RUN mkdir /app

WORKDIR /app

EXPOSE 8000

CMD ["/entrypoint.sh"]
