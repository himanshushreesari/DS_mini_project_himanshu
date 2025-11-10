@echo off
REM Quick Start Script for Population Deposits Dashboard (Windows)
REM This script sets up and launches the Streamlit dashboard

echo =========================================
echo Population Deposits Analysis Dashboard
echo =========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python 3 is not installed. Please install Python 3.11 or higher.
    pause
    exit /b 1
)

echo Python found: 
python --version
echo.

REM Check if we're in the right directory
if not exist "app.py" (
    echo ERROR: app.py not found. Please run this script from the streamlit_app directory.
    pause
    exit /b 1
)

echo Located in correct directory
echo.

REM Check if virtual environment exists
if not exist "venv" (
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
echo Virtual environment activated
echo.

REM Install/upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip --quiet
echo Pip upgraded
echo.

REM Install requirements
echo Installing required packages...
if exist "requirements.txt" (
    pip install -r requirements.txt --quiet
    echo All packages installed
) else (
    echo ERROR: requirements.txt not found!
    pause
    exit /b 1
)
echo.

REM Check if data files exist
echo Checking for data files...
if exist "..\data\processed" (
    if exist "..\data\processed\cleaned_data.csv" (
        if exist "..\data\processed\featured_data.csv" (
            echo Data files found
        ) else (
            echo WARNING: featured_data.csv not found
        )
    ) else (
        echo WARNING: cleaned_data.csv not found
    )
) else (
    echo WARNING: Data directory not found
    echo Please ensure the project structure is correct.
)
echo.

REM Check if model files exist
echo Checking for model files...
if exist "..\models\saved_models" (
    echo Model directory found
) else (
    echo WARNING: Model directory not found
)
echo.

REM Launch Streamlit
echo =========================================
echo Launching Streamlit Dashboard...
echo =========================================
echo.
echo The dashboard will open in your browser at:
echo http://localhost:8501
echo.
echo Press Ctrl+C to stop the server
echo.

streamlit run app.py
