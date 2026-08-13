#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR" && pwd)"
mkdir -p "$ROOT_DIR/logs"
cd "$ROOT_DIR/infosecdairies/infosec-backend/backend"
exec .venv/bin/python manage.py runserver 0.0.0.0:8000 --noreload >> "$ROOT_DIR/logs/django_8000.log" 2>&1
