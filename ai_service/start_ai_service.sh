#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
mkdir -p "$ROOT_DIR/logs"
cd "$SCRIPT_DIR"
pkill -f "uvicorn app.main" 2>/dev/null
sleep 3
setsid nohup .venv/bin/python -m uvicorn app.main:app --host 0.0.0.0 --port 8001 >> "$ROOT_DIR/logs/ai_service_8001.log" 2>&1 < /dev/null &
disown
echo "started pid $!"