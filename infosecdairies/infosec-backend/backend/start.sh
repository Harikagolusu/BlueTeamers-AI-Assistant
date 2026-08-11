#!/bin/bash

python manage.py migrate

gunicorn backend.wsgi:application \
  --bind 0.0.0.0:$PORT \
  --access-logfile - \
  --error-logfile - \
  --capture-output \
  --log-level info
