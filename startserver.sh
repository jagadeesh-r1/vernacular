#!/usr/bin/env bash
ls

python3 /app/validate/manage.py check --deploy

python3 validate/manage.py runserver 0.0.0.0:5001