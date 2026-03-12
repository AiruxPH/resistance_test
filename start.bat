@echo off
setlocal
title Resistance Test Bootstrap

echo [*] Checking for Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] FATAL ERROR: Python is not installed or not in PATH.
    echo [!] This tool requires Python 3.x to run.
    echo.
    echo [*] Opening Python download page for you...
    start https://www.python.org/downloads/
    echo.
    echo Finish the installation and make sure to check "Add Python to PATH".
    echo Then run this script again.
    pause
    exit /b
)

echo [*] Python detected. Launching Resistance Test...
python run.py

if %errorlevel% neq 0 (
    echo.
    echo [-] An error occurred during execution. 
    echo Please check if 'requirements.txt' exists and your internet is connected.
    pause
)

endlocal
