@echo off
REM ============================================================
REM  Hardfox v4.0 - Firefox Hardening Tool
REM  Launcher Script
REM ============================================================

title Hardfox v4.0 Launcher

echo.
echo ============================================================
echo  Hardfox v4.0 - Firefox Hardening Tool
echo  Clean Architecture Edition
echo ============================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH
    echo.
    echo Please install Python 3.9+ from https://www.python.org/
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

REM Display Python version
for /f "tokens=*" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo [OK] %PYTHON_VERSION%
echo.
echo ============================================================
echo  Launching Hardfox v4.0...
echo ============================================================

REM Launch the GUI application
python hardfox_gui.py %*

REM Show exit status
if %errorlevel% neq 0 (
    echo.
    echo ============================================================
    echo  Application exited with error code: %errorlevel%
    echo ============================================================
    echo.
    pause
)
