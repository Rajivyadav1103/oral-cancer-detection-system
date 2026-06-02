@echo off
REM Start the React Frontend

echo.
echo ====================================
echo Starting React Frontend
echo ====================================
echo.

cd frontend

if not exist "node_modules" (
    echo Dependencies not found. Installing...
    npm install
)

echo Starting development server (port 3000)...
echo.
npm start
