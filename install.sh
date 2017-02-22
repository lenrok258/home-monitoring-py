#!/usr/bin/env bash

virtualenv .env

.env/bin/pip install -r requirements.txt

IS_PI_ENV=$(cat config/config.json | grep '"rpi-env": true')
if [[ ${IS_PI_ENV} ]]; then
    .env/bin/pip install Adafruit_Python_DHT
fi;
