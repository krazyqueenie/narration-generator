@echo off
setlocal
cd /d "%~dp0"
title Narration Generator - Updated

echo Starting Narration Generator...
echo Closing any previous local narrator on port 5050...
powershell -NoProfile -ExecutionPolicy Bypass -Command "try { Invoke-WebRequest -UseBasicParsing -Method POST -Uri 'http://127.0.0.1:5050/shutdown' -TimeoutSec 1 | Out-Null } catch {}" >nul 2>&1
timeout /t 2 /nobreak >nul

echo Keep this window open while using the narrator.
python narrate_web.py
pause
