FROM alpine:3.18

RUN apk update && apk upgrade && apk add python3 py3-pip tzdata libpq

COPY --chmod=777 requirements.txt /requirements.txt

RUN pip3 install -r requirements.txt

COPY --chmod=777 entrypoint.sh /entrypoint.sh

RUN mkdir -p /app/backend

WORKDIR /app/backend

EXPOSE 8000

ENTRYPOINT ["sh", "/entrypoint.sh"]
