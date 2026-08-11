@echo off
echo Starting AI Service Backend...
cd ai_service
call uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
