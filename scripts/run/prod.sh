#!/bin/bash

sleep 20
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py collectstatic --no-input
gunicorn -b :8000 hospital-triage.wsgi
