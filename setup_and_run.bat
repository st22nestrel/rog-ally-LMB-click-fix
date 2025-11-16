@echo off
echo ========================================
echo ROG Ally Click Converter Setup
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/
    pause
    exit /b 1
)

echo Installing required packages...
pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo ERROR: Failed to install packages
    pause
    exit /b 1
)

echo.
echo ========================================
echo Starting Click Converter...
echo ========================================
echo.

python click_converter.py

pause

