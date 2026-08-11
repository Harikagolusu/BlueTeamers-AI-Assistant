@echo off
echo Starting Django Backend (infosec-backend) on port 8000...
cd infosecdairies\infosec-backend\backend
call python manage.py migrate
call python manage.py loaddata courses/fixtures/courses.json
call python manage.py runserver 8000
