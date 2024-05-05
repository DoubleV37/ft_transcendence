FROM alpine:3.18

RUN apk update && apk upgrade && apk add python3 py3-pip

RUN pip3 install websockets[12.0]

RUN mkdir -p /Server

WORKDIR /Server

CMD ["python3", "-u", "server.py"]
