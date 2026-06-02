@echo off
REM Start the Oral Cancer Detection System

echo.
echo ====================================
echo Starting Oral Cancer Detection
echo ====================================
echo.

REM Check if model exists
if not exist "models\oral_cancer_model.h5" (
    echo ERROR: Model not found at models\oral_cancer_model.h5
    echo Please run: python train_model.py
    pause
    exit /b 1
)

echo Starting Backend API (port 8000)...
echo.
python app.py
