@echo off
setlocal
cd /d "%~dp0"
title Narration Generator Setup
python -m pip install -r requirements.txt
if errorlevel 1 (
  echo.
  echo Setup failed. Check the error above.
  pause
  exit /b 1
)
echo.
echo Setup complete. Run "2. Start Narration Tool.bat".
pause
