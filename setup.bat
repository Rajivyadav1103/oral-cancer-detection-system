@echo off
REM Oral Cancer Detection - Automated Setup Script for Windows

echo.
echo ====================================
echo Oral Cancer Detection System Setup
echo ====================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from https://www.python.org
    pause
    exit /b 1
)

REM Check if pip is available
pip --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: pip is not available
    pause
    exit /b 1
)

echo [1/3] Installing Python dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install Python dependencies
    pause
    exit /b 1
)
echo [✓] Python dependencies installed

echo.
echo [2/3] Setting up frontend...
cd frontend
if errorlevel 1 (
    echo ERROR: frontend directory not found
    pause
    exit /b 1
)

REM Check if Node is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo WARNING: Node.js is not installed or not in PATH
    echo Please install Node.js from https://nodejs.org
    pause
    exit /b 1
)

npm install
if errorlevel 1 (
    echo ERROR: Failed to install Node dependencies
    pause
    exit /b 1
)
echo [✓] Frontend dependencies installed

cd ..

echo.
echo [3/3] Training the model...
echo NOTE: This will take 15-30 minutes depending on your hardware
echo.
python train_model.py
if errorlevel 1 (
    echo ERROR: Model training failed
    pause
    exit /b 1
)
echo [✓] Model trained successfully

echo.
echo ====================================
echo Setup Complete!
echo ====================================
echo.
echo Next steps:
echo 1. Start the backend:
echo    python app.py
echo.
echo 2. In a new terminal, start the frontend:
echo    cd frontend
echo    npm start
echo.
echo 3. Open browser to http://localhost:3000
echo.
pause
