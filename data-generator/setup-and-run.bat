@echo off
setlocal enabledelayedexpansion

echo ========================================
echo Azure Data Analytics - Data Generator
echo ========================================
echo.

:: Check if Python is installed
echo [1/5] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found!
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)
echo ✓ Python found:
python --version

:: Check if pip is available
echo.
echo Checking pip...
python -m pip --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: pip not found!
    pause
    exit /b 1
)
echo ✓ pip is available

:: Create virtual environment
echo.
echo [2/5] Setting up virtual environment...
if exist "venv" (
    echo ✓ Virtual environment already exists, removing old one...
    rmdir /s /q venv
)

echo Creating new virtual environment...
python -m venv venv
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment
    pause
    exit /b 1
)
echo ✓ Virtual environment created successfully

:: Activate virtual environment
echo.
echo [3/5] Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)
echo ✓ Virtual environment activated

:: Install dependencies from requirements.txt
echo.
echo [4/5] Installing dependencies from requirements.txt...
if not exist "requirements.txt" (
    echo ERROR: requirements.txt not found!
    echo Creating requirements.txt with default dependencies...
    echo Flask==2.3.3> requirements.txt
    echo pandas==2.1.1>> requirements.txt
    echo faker==19.6.2>> requirements.txt
    echo pyarrow==13.0.0>> requirements.txt
    echo Werkzeug==2.3.7>> requirements.txt
)

echo Installing packages using pip...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    echo Trying to install packages individually...
    python -m pip install Flask==2.3.3
    python -m pip install pandas==2.1.1
    python -m pip install faker==19.6.2
    python -m pip install pyarrow==13.0.0
    python -m pip install Werkzeug==2.3.7
    if errorlevel 1 (
        echo ERROR: Failed to install dependencies with alternative method
        pause
        exit /b 1
    )
)
echo ✓ All dependencies installed successfully

:: Verify installation
echo.
echo Verifying installation...
python -c "import flask, pandas, faker, pyarrow; print('✓ All packages imported successfully')"
if errorlevel 1 (
    echo WARNING: Some packages may not be properly installed
    echo Continuing anyway...
)

:: Create necessary directories
echo.
echo Setting up directories...
if not exist "temp" (
    mkdir temp
    echo ✓ Created temp directory
) else (
    echo ✓ Temp directory already exists
)

if not exist "templates" (
    echo WARNING: templates directory not found
    echo Make sure templates/index.html exists
)

:: Check if app.py exists
if not exist "app.py" (
    echo ERROR: app.py not found in current directory
    echo Please make sure you're running this script from the data-generator folder
    echo Current directory: %CD%
    pause
    exit /b 1
)

:: Display system information
echo.
echo System Information:
echo Python version:
python --version
echo Flask version:
python -c "import flask; print('Flask', flask.__version__)"
echo Pandas version:
python -c "import pandas; print('Pandas', pandas.__version__)"

:: Run the Flask application
echo.
echo [5/5] Starting Flask Data Generator...
echo.
echo ========================================
echo   🚀 Data Generator is starting...
echo.
echo   📊 Generate realistic data for:
echo   • Salesforce CRM
echo   • Salesforce Marketing Cloud (SFMC)  
echo   • NetSuite ERP
echo.
echo   🌐 Access the application at:
echo   http://localhost:5000
echo.
echo   📁 Generated files will be saved to:
echo   %CD%\temp\
echo ========================================
echo.
echo Press Ctrl+C to stop the application
echo.

:: Set Flask environment variables
set FLASK_APP=app.py
set FLASK_ENV=development
set FLASK_DEBUG=1

:: Run the application
python app.py

:: Cleanup message
echo.
echo ========================================
echo 🛑 Application stopped
echo ========================================
echo.
echo Generated files are available in the temp folder
echo Virtual environment is still active
echo.
echo To deactivate virtual environment, run: deactivate
echo To restart the application, run: python app.py
echo.
pause