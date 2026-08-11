#!/bin/bash
# Start FastAPI AI Service on port 8001
cd /home/harika/BlueTeamers-AI-Assistant/ai_service
exec .venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8001 >> /home/harika/BlueTeamers-AI-Assistant/logs/ai_service_8001.log 2>&1