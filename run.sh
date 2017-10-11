#!/usr/bin/env bash

cd $(dirname $0)

#PYTHONDONTWRITEBYTECODE = don't write .pyc files 
PYTHONDONTWRITEBYTECODE=1 .env/bin/python -u run.py
