@echo off
echo 🚀 Starting Miami Med Spa Voice AI API Server...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.10 or higher.
    pause
    exit /b 1
)

REM Install dependencies
echo 📦 Checking dependencies...
pip install -r requirements.txt

echo.
echo ✓ Dependencies ready
echo.
echo 🌐 Starting API server on http://localhost:8000
echo.
echo API will be available at:
echo   - Health check: http://localhost:8000/
echo   - Services: http://localhost:8000/services
echo   - Docs: http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop the server
echo.

REM Start the server
python api_server.py
