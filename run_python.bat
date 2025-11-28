@echo off
echo ========================================
echo ROG Ally Click Converter - Optimized Python Version
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

echo This optimized version uses XInput API directly.
echo No additional packages needed!
echo.
echo Expected CPU usage: ^<2%% (vs 8%% for inputs library)
echo.
echo ========================================
echo Starting Optimized Click Converter...
echo ========================================
echo.

python click_converter_xinput/click_converter.py

pause

