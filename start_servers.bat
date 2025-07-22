@echo off
echo Starting AI Air Quality Agent...
echo.

echo Starting Backend Server...
cd /d "e:\Agent\ai-air-quality-agent\backend"
start "Backend" cmd /k "python -m uvicorn main:app --reload --port 8000"

echo.
echo Waiting 5 seconds for backend to start...
timeout /t 5 /nobreak > nul

echo Starting Frontend...
cd /d "e:\Agent\ai-air-quality-agent\frontend"
start "Frontend" cmd /k "npm start"

echo.
echo Both servers should be starting...
echo Backend: http://localhost:8000
echo Frontend: http://localhost:3000
echo.
pause
