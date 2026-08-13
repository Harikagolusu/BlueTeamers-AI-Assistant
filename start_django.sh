#!/bin/bash
# Start Django Backend on port 8000
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR" && pwd)"
mkdir -p "$ROOT_DIR/logs"
cd "$ROOT_DIR/infosecdairies/infosec-backend/backend"
if [ -x ".venv/bin/python" ]; then
  exec .venv/bin/python manage.py runserver 0.0.0.0:8000 --noreload >> "$ROOT_DIR/logs/django_8000.log" 2>&1
else
  exec python manage.py runserver 0.0.0.0:8000 --noreload >> "$ROOT_DIR/logs/django_8000.log" 2>&1
fi