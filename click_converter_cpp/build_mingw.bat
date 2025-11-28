@echo off
REM Build script specifically for MinGW G++

echo Building with MinGW G++...
g++.exe -std=c++17 -O2 -o click_converter.exe click_converter.cpp -lXInput -lUser32 -static

if %errorlevel% neq 0 (
    echo Build failed!
    pause
    exit /b 1
)

echo.
echo Build successful! Run click_converter.exe
pause

