@echo off
echo ========================================
echo Azure Data Analytics - Data Generator
echo ========================================
echo.

:: Check if virtual environment exists
if not exist "venv" (
    echo Virtual environment not found!
    echo Please run setup-and-run.bat first to create the environment
    pause
    exit /b 1
)

:: Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

:: Check if app.py exists
if not exist "app.py" (
    echo ERROR: app.py not found
    pause
    exit /b 1
)

:: Create temp directory if needed
if not exist "temp" mkdir temp

:: Start the application
echo.
echo 🚀 Starting Data Generator...
echo 🌐 Open http://localhost:5000 in your browser
echo.
echo Press Ctrl+C to stop
echo.

python app.py