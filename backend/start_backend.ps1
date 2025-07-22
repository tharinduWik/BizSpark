# PowerShell script to start the Air Quality AI Agent Backend
Write-Host "🌍 Starting Air Quality AI Agent Backend..." -ForegroundColor Green

# Navigate to backend directory
Set-Location "e:\Agent\ai-air-quality-agent\backend"

# Install dependencies
Write-Host "📦 Installing dependencies..." -ForegroundColor Yellow
pip install fastapi uvicorn python-dotenv pandas openai

# Start the server
Write-Host "🚀 Starting server on http://localhost:8000..." -ForegroundColor Cyan
Write-Host "📋 API Documentation will be available at: http://localhost:8000/docs" -ForegroundColor Blue
Write-Host "💚 Health Check: http://localhost:8000/health" -ForegroundColor Blue
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Red

try {
    python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
} catch {
    Write-Host "❌ Failed to start server: $_" -ForegroundColor Red
    Write-Host "Trying alternative method..." -ForegroundColor Yellow
    python main.py
}

Read-Host "Press Enter to exit"
