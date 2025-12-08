@echo off
REM Keep window open on errors
setlocal enabledelayedexpansion

echo Starting Parking Vision Application...
echo.

REM Get the directory where this batch file is located and go to project root
cd /d "%~dp0.."
set "PROJECT_ROOT=%CD%"

echo Project root: %PROJECT_ROOT%
echo.

REM Check if virtual environment exists
if not exist "%PROJECT_ROOT%\.venv\Scripts\activate.bat" (
    echo.
    echo ========================================
    echo ERROR: Virtual environment not found!
    echo ========================================
    echo Please ensure .venv folder exists in the project root.
    echo Expected location: %PROJECT_ROOT%\.venv
    echo.
    echo To create a virtual environment, run:
    echo   python -m venv .venv
    echo.
    pause
    exit /b 1
)

REM Activate virtual environment
echo Activating virtual environment...
call "%PROJECT_ROOT%\.venv\Scripts\activate.bat"
if errorlevel 1 (
    echo.
    echo ========================================
    echo ERROR: Failed to activate virtual environment!
    echo ========================================
    echo Please check that the virtual environment is properly set up.
    echo.
    pause
    exit /b 1
)
echo Virtual environment activated successfully.

REM Go to Deployment folder
cd /d "%PROJECT_ROOT%\Deployment"
if errorlevel 1 (
    echo.
    echo ========================================
    echo ERROR: Failed to navigate to Deployment folder!
    echo ========================================
    echo Expected location: %PROJECT_ROOT%\Deployment
    echo.
    pause
    exit /b 1
)
echo Working directory: %CD%
echo.

REM Check if streamlit is installed
echo Checking for Streamlit...
python -c "import streamlit" 2>nul
if errorlevel 1 (
    echo Streamlit not found. Installing...
    pip install streamlit
    if errorlevel 1 (
        echo ERROR: Failed to install Streamlit!
        echo.
        pause
        exit /b 1
    )
) else (
    echo Streamlit is installed.
)


echo.
echo All checks passed. Starting Streamlit application...
echo The application will open in your default browser.
echo Press Ctrl+C to stop the application.
echo.

REM Run Streamlit - don't pause after this since streamlit keeps running
streamlit run streamlit_app.py

REM If we get here, streamlit has exited
echo.
echo Streamlit application has stopped.
pause

