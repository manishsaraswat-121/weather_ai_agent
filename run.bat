@echo off
REM AI Agent Pipeline - Quick Start Script for Windows

echo ========================================
echo AI Agent Pipeline - Quick Start
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.9 or higher
    pause
    exit /b 1
)

echo Python found
python --version
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
    echo Virtual environment created
) else (
    echo Virtual environment already exists
)
echo.

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo.

REM Install dependencies
echo Installing dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt
echo Dependencies installed
echo.

REM Check for .env file
if not exist ".env" (
    echo WARNING: .env file not found!
    echo Creating .env from template...
    copy .env.example .env
    echo.
    echo IMPORTANT: Please edit .env and add your API keys:
    echo    - OPENAI_API_KEY
    echo    - OPENWEATHER_API_KEY
    echo    - LANGSMITH_API_KEY (optional)
    echo.
    echo Press any key after you've updated the .env file...
    pause >nul
)

echo API keys should be configured in .env
echo.

REM Ask user what to run
echo What would you like to do?
echo 1) Run Streamlit UI (Recommended)
echo 2) Run Tests
echo 3) Both
echo.
set /p choice="Enter choice (1-3): "

if "%choice%"=="1" goto streamlit
if "%choice%"=="2" goto tests
if "%choice%"=="3" goto both
echo Invalid choice
pause
exit /b 1

:streamlit
echo.
echo Starting Streamlit UI...
echo Open your browser at http://localhost:8501
echo.
streamlit run app.py
goto end

:tests
echo.
echo Running tests...
python -m pytest test_main.py -v --cov=main --cov-report=term-missing
pause
goto end

:both
echo.
echo Running tests first...
python -m pytest test_main.py -v
echo.
echo Tests completed
echo.
echo Starting Streamlit UI...
echo Open your browser at http://localhost:8501
echo.
streamlit run app.py
goto end

:end
echo.
echo Exiting...