@echo off
setlocal
cd /d "%~dp0"
title Narration Generator Setup

echo Setting up Narration Generator...
echo.
echo This installs the Python packages needed to run the source version.
echo You only need to run this once, or again if requirements change.
echo.

python -m pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo Setup failed.
    pause
    exit /b 1
)

echo.
echo Setup complete.
echo.
pause
