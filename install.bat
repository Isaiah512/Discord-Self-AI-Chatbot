@echo off
setlocal enabledelayedexpansion

echo ===================================================
echo Discord Self AI Chatbot - Windows Installation Script
echo ===================================================

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not detected. Preparing to download and install Python 3.9...
    
    REM Detect system architecture
    if "%PROCESSOR_ARCHITECTURE%"=="AMD64" (
        set PYTHON_URL=https://www.python.org/ftp/python/3.9.13/python-3.9.13-amd64.exe
        set PYTHON_FILENAME=python-3.9.13-amd64.exe
    ) else (
        set PYTHON_URL=https://www.python.org/ftp/python/3.9.13/python-3.9.13.exe
        set PYTHON_FILENAME=python-3.9.13.exe
    )

    REM Download Python installer
    echo Downloading Python installer...
    powershell -Command "Invoke-WebRequest -Uri '%PYTHON_URL%' -OutFile '%PYTHON_FILENAME%'"

    REM Install Python
    echo Installing Python...
    start /wait %PYTHON_FILENAME% /quiet InstallAllUsers=1 PrependPath=1 Include_test=0

    REM Clean up installer
    del %PYTHON_FILENAME%

    REM Refresh environment variables
    refreshenv >nul 2>&1
)

REM Verify Python installation
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Failed to install Python. Please install manually from python.org
    pause
    exit /b 1
)

REM Create installation directory
if not exist "discord-ai-chatbot" mkdir discord-ai-chatbot
cd discord-ai-chatbot

REM Create and activate virtual environment
echo Creating virtual environment...
python -m venv venv

echo Activating virtual environment...
call venv\Scripts\activate

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install requirements
echo Installing project dependencies...
pip install discord.py python-dotenv langchain langchain-google-genai google-generativeai Pillow aiohttp requests

REM Clone the project repository
echo Downloading project files...
powershell -Command "git clone https://github.com/isaiah76/Discord-Self-AI-Chatbot.git ."

REM Create .env file template
echo Creating .env file template...
(
    echo DISCORD_TOKEN=your_discord_token_here
    echo GEMINI_API_KEY=your_gemini_api_key_here
    echo HF_API_TOKEN=your_huggingface_api_token_here
) > .env

echo ===================================================
echo Installation Complete!
echo 1. Open .env and fill in your tokens
echo 2. Activate venv with: venv\Scripts\activate
echo 3. Run the bot with: python main.py
echo ===================================================

pause
