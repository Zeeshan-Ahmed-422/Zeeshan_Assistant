@echo off
echo ============================================
echo   ZEESHAN Voice Assistant Setup
echo ============================================
echo.

REM Check Python installation
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed!
    echo Please install Python 3.10.6 from python.org
    pause
    exit /b 1
)

echo [1/4] Python found!
python --version

REM Create virtual environment
echo.
echo [2/4] Creating virtual environment...
python -m venv venv
call venv\Scripts\activate.bat

REM Install dependencies
echo.
echo [3/4] Installing dependencies...
echo This may take a few minutes...
pip install --upgrade pip
pip install -r requirements.txt

REM Setup configuration
echo.
echo [4/4] Setting up configuration...
if not exist .env (
    copy .env.example .env
    echo Created .env file - Please edit it with your API key!
)

REM Create directories
if not exist data mkdir data
if not exist logs mkdir logs

echo.
echo ============================================
echo   Setup Complete!
echo ============================================
echo.
echo Next steps:
echo 1. Edit .env file and add your API key
echo 2. Run: python main.py
echo.
echo For help, check README.md or QUICKSTART.md
echo ============================================
pause