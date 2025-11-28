@echo off
REM Build script specifically for Microsoft Visual C++ (MSVC)
REM Run this from a "Developer Command Prompt for VS" or after running vcvarsall.bat

echo Building with MSVC...
cl.exe /EHsc /O2 /std:c++17 click_converter.cpp /Fe:click_converter.exe /link XInput.lib User32.lib

if %errorlevel% neq 0 (
    echo Build failed!
    pause
    exit /b 1
)

echo.
echo Build successful! Run click_converter.exe
pause

