#!/bin/bash
# Start React Frontend on port 5173
cd /home/harika/BlueTeamers-AI-Assistant/infosecdairies
export PATH="/home/harika/BlueTeamers-AI-Assistant/infosecdairies/node_modules/.bin:$PATH"
exec npm run dev -- --port 5173 >> /home/harika/BlueTeamers-AI-Assistant/logs/frontend_5173.log 2>&1