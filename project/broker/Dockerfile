FROM python:3-alpine

WORKDIR /usr/src/app

RUN apk add mosquitto

COPY requirements.txt ./
COPY mosquitto/ /etc/mosquitto/

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD mosquitto -c /etc/mosquitto/mosquitto.conf
