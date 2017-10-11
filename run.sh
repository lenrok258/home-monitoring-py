#!/usr/bin/env bash

cd $(dirname $0)

PYTHONDONTWRITEBYTECODE=1 .env/bin/python -u run.py
