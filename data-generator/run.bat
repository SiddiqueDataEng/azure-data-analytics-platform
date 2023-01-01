@echo off
setlocal enabledelayedexpansion

echo ========================================
echo Azure Data Analytics - Data Generator
echo ========================================
echo.

:: Check if UV is installed
echo [1/6] Checking UV package installer...
uv --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: UV package installer not found!
    echo Please install UV first: https://docs.astral.sh/uv/getting-started/installation/
    echo.
    echo Quick install options:
    echo   - PowerShell: powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
    echo   - Scoop: scoop install uv
    echo   - Chocolatey: choco install uv
    echo.
    pause
    exit /b 1
)
echo ✓ UV package installer found

:: Create virtual environment
echo.
echo [2/6] Creating virtual environment...
if exist "venv" (
    echo ✓ Virtual environment already exists
) else (
    uv venv venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
    echo ✓ Virtual environment created successfully
)

:: Activate virtual environment
echo.
echo [3/6] Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)
echo ✓ Virtual environment activated

:: Install dependencies
echo.
echo [4/6] Installing dependencies...
echo Installing Flask and required packages...
uv pip install Flask==2.3.3
if errorlevel 1 (
    echo ERROR: Failed to install Flask
    pause
    exit /b 1
)

echo Installing pandas...
uv pip install pandas==2.1.1
if errorlevel 1 (
    echo ERROR: Failed to install pandas
    pause
    exit /b 1
)

echo Installing faker...
uv pip install faker==19.6.2
if errorlevel 1 (
    echo ERROR: Failed to install faker
    pause
    exit /b 1
)

echo Installing pyarrow...
uv pip install pyarrow==13.0.0
if errorlevel 1 (
    echo ERROR: Failed to install pyarrow
    pause
    exit /b 1
)

echo Installing Werkzeug...
uv pip install Werkzeug==2.3.7
if errorlevel 1 (
    echo ERROR: Failed to install Werkzeug
    pause
    exit /b 1
)

echo ✓ All dependencies installed successfully

:: Create temp directory if it doesn't exist
echo.
echo [5/6] Setting up directories...
if not exist "temp" (
    mkdir temp
    echo ✓ Created temp directory
) else (
    echo ✓ Temp directory already exists
)

:: Check if app.py exists
if not exist "app.py" (
    echo ERROR: app.py not found in current directory
    echo Please make sure you're running this script from the data-generator folder
    pause
    exit /b 1
)

:: Run the Flask application
echo.
echo [6/6] Starting Flask application...
echo.
echo ========================================
echo   Data Generator is starting...
echo   Access the application at:
echo   http://localhost:5000
echo ========================================
echo.
echo Press Ctrl+C to stop the application
echo.

python app.py

:: Cleanup message
echo.
echo ========================================
echo Application stopped
echo ========================================
echo.
pause