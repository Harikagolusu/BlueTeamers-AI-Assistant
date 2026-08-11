#!/bin/bash
# Start Django Backend on port 8000
cd /home/harika/BlueTeamers-AI-Assistant/infosecdairies/infosec-backend/backend
python manage.py runserver 0.0.0.0:8000 --noreload >> /home/harika/BlueTeamers-AI-Assistant/logs/django_8000.log 2>&1