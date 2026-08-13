#!/bin/bash
cd /home/harika/BlueTeamers-AI-Assistant/ai_service
pkill -f "uvicorn app.main" 2>/dev/null
sleep 3
setsid nohup .venv/bin/python -m uvicorn app.main:app --host 0.0.0.0 --port 8001 >> /tmp/ai_service.log 2>&1 < /dev/null &
disown
echo "started pid $!"