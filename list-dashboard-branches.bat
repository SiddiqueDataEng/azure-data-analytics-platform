@echo off
SETLOCAL ENABLEDELAYEDEXPANSION

echo ========================================
echo === DASHBOARD BRANCHES OVERVIEW ===
echo ========================================
echo.

REM Load configuration
if exist "master-config.bat" (
    call master-config.bat
) else (
    set "MASTER_GITHUB_USER=SiddiqueDataEng"
    set "DEFAULT_REPO_NAME=azure-data-analytics-platform"
)

REM Project detection
call :DetectProjectName REPO_NAME
echo Repository: %REPO_NAME%
echo Master Account: %MASTER_GITHUB_USER%
echo.

REM Check if we're in a git repository
git status >nul 2>&1
if !ERRORLEVEL! neq 0 (
    echo ❌ Not in a Git repository or Git not available
    echo.
    echo To check remote branches, ensure you're in the project directory
    echo and have Git installed.
    pause
    exit /b 1
)

echo ========================================
echo === LOCAL DASHBOARD BRANCHES ===
echo ========================================
echo.

REM List local dashboard branches
git branch | findstr "dashboard" >nul 2>&1
if !ERRORLEVEL! equ 0 (
    echo Local dashboard branches:
    git branch | findstr "dashboard"
) else (
    echo ❌ No local dashboard branches found
)

echo.
echo ========================================
echo === REMOTE DASHBOARD BRANCHES ===
echo ========================================
echo.

REM Fetch latest remote information
echo Fetching latest branch information...
git fetch origin >nul 2>&1

REM List remote dashboard branches
git branch -r | findstr "dashboard" >nul 2>&1
if !ERRORLEVEL! equ 0 (
    echo Remote dashboard branches:
    git branch -r | findstr "dashboard"
    echo.
    
    REM Count dashboard branches
    for /f %%i in ('git branch -r ^| findstr "dashboard" ^| find /c /v ""') do set BRANCH_COUNT=%%i
    echo Total dashboard branches: !BRANCH_COUNT!
) else (
    echo ❌ No remote dashboard branches found
    echo.
    echo This could mean:
    echo 1. No dashboard branches have been created yet
    echo 2. You need to run: create-dashboard-branch.bat
    echo 3. Remote repository doesn't exist or isn't accessible
)

echo.
echo ========================================
echo === BRANCH DETAILS ===
echo ========================================
echo.

REM Show detailed information for each dashboard branch
for /f "tokens=*" %%a in ('git branch -r ^| findstr "dashboard" 2^>nul') do (
    set "BRANCH_NAME=%%a"
    set "BRANCH_NAME=!BRANCH_NAME:~9!"
    echo Branch: !BRANCH_NAME!
    
    REM Get last commit info
    git log origin/!BRANCH_NAME! -1 --pretty=format:"  Last commit: %%h - %%s (%%ad)" --date=short 2>nul
    echo.
    echo.
)

echo ========================================
echo === QUICK ACTIONS ===
echo ========================================
echo.
echo Available actions:
echo 1. Create new dashboard branch: create-dashboard-branch.bat
echo 2. Test dashboard prerequisites: test-dashboard-branch.bat
echo 3. Switch to dashboard branch: git checkout [branch-name]
echo 4. View branch on GitHub: https://github.com/%MASTER_GITHUB_USER%/%REPO_NAME%/branches
echo.

REM Show GitHub URLs for easy access
echo GitHub Repository: https://github.com/%MASTER_GITHUB_USER%/%REPO_NAME%
echo GitHub Branches: https://github.com/%MASTER_GITHUB_USER%/%REPO_NAME%/branches
echo.

pause
ENDLOCAL
exit /b

:DetectProjectName
set "DETECTED_NAME=azure-data-analytics-platform"

if exist "data-generator\app.py" (
    if exist "infrastructure\bicep\main.bicep" (
        if exist "powerbi\data-model-design.md" (
            set "DETECTED_NAME=azure-data-analytics-platform"
        )
    )
)

if exist "README.md" (
    findstr /i "Azure Data Analytics Platform" README.md >nul 2>&1
    if !ERRORLEVEL! equ 0 (
        set "DETECTED_NAME=azure-data-analytics-platform"
    )
)

set "%~1=%DETECTED_NAME%"
exit /b