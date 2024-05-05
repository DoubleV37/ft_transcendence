FROM alpine:3.18

RUN apk update && apk upgrade && apk add python3 py3-pip

RUN mkdir -p /Server

WORKDIR /Server

COPY --chmod=777 requirements.txt /Server/requirements.txt

RUN pip3 install -r ./requirements.txt


CMD ["python3", "-u", "server.py"]
