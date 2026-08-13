#!/bin/bash
# Resolve the repo root from this script's own location (works for any user).
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR" && pwd)"

mkdir -p "$ROOT_DIR/logs"

echo "Starting BlueTeamers AI Assistant Platform..."
echo ""
echo "Starting Django Backend (port 8000)..."
( cd "$ROOT_DIR" && bash start_django.sh ) &
sleep 3
echo "Starting FastAPI AI Service (port 8001)..."
( cd "$ROOT_DIR" && bash start_backend.sh ) &
sleep 3
echo "Starting React Frontend (port 5173)..."
( cd "$ROOT_DIR" && bash start_frontend.sh ) &
sleep 3
echo ""
echo "All services started in background."
echo "Frontend: http://localhost:5173"
echo "Django API: http://localhost:8000"
echo "FastAPI AI Service: http://localhost:8001"
echo "FastAPI Docs: http://localhost:8001/docs"
