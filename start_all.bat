@echo off
echo Starting BlueTeamers AI Assistant Platform...
start cmd /k "call start_django.bat"
start cmd /k "call start_ollama.bat"
start cmd /k "call start_backend.bat"
start cmd /k "call start_frontend.bat"
echo All services started in separate windows.
