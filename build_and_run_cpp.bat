@echo off
echo ========================================
echo ROG Ally Click Converter - Build Script
echo ========================================
echo.

REM Try to detect which compiler is available

REM Check for MSVC (Visual Studio)
where cl.exe >nul 2>&1
if %errorlevel% == 0 (
    echo Found: Microsoft Visual C++ Compiler
    goto :build_msvc
)

REM Check for MinGW g++
where g++.exe >nul 2>&1
if %errorlevel% == 0 (
    echo Found: MinGW G++ Compiler
    goto :build_mingw
)

REM Check for Clang
where clang++.exe >nul 2>&1
if %errorlevel% == 0 (
    echo Found: Clang++ Compiler
    goto :build_clang
)

REM No compiler found
echo ERROR: No C++ compiler found!
echo.
echo Please install one of the following:
echo   1. Visual Studio (with C++ tools)
echo   2. MinGW-w64 (https://www.mingw-w64.org/)
echo   3. LLVM/Clang (https://releases.llvm.org/)
echo.
echo Or use the pre-built executable if available.
echo.
pause
exit /b 1

:build_msvc
echo.
echo Building with MSVC...
cl.exe /EHsc /O2 /std:c++17 click_converter_cpp/click_converter.cpp /Fe:click_converter.exe /link XInput.lib User32.lib
if %errorlevel% neq 0 (
    echo.
    echo Build failed!
    pause
    exit /b 1
)
goto :build_success

:build_mingw
echo.
echo Building with MinGW G++...
g++.exe -std=c++17 -O2 -o click_converter.exe click_converter_cpp/click_converter.cpp -lXInput -lUser32 -static
if %errorlevel% neq 0 (
    echo.
    echo Build failed!
    pause
    exit /b 1
)
goto :build_success

:build_clang
echo.
echo Building with Clang++...
clang++.exe -std=c++17 -O2 -o click_converter.exe click_converter_cpp/click_converter.cpp -lXInput -lUser32
if %errorlevel% neq 0 (
    echo.
    echo Build failed!
    pause
    exit /b 1
)
goto :build_success

:build_success
echo.
echo ========================================
echo Build successful!
echo ========================================
echo.
echo Starting click_converter.exe...
echo.
echo ========================================
echo.

click_converter.exe

pause

