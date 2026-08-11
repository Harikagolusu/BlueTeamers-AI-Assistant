#!/bin/bash
# One-time local dev setup: apply all migrations and seed course data.
set -e
python manage.py migrate
python manage.py loaddata courses/fixtures/courses.json
echo "Dev setup complete. Run: python manage.py runserver"
