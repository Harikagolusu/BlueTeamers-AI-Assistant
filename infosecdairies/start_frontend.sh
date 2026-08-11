#!/bin/bash
cd /home/harika/BlueTeamers-AI-Assistant/infosecdairies
export PATH="/home/harika/BlueTeamers-AI-Assistant/infosecdairies/node_modules/.bin:$PATH"
exec npm run dev >> /home/harika/BlueTeamers-AI-Assistant/logs/frontend_8081.log 2>&1
