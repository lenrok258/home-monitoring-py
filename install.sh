#!/usr/bin/env bash

virtualenv .env

.env/bin/pip install -r requirements.txt
.env/bin/pip install Adafruit_Python_DHT
