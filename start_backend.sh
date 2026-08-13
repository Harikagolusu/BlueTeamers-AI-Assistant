#!/bin/bash
# Start FastAPI AI Service on port 8001
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR" && pwd)"
mkdir -p "$ROOT_DIR/logs"
cd "$ROOT_DIR/ai_service"
exec .venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8001 >> "$ROOT_DIR/logs/ai_service_8001.log" 2>&1