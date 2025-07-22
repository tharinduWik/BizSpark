# Start-AirQualityAgent.ps1
# PowerShell script to start the Air Quality Agent system with Gemini

Write-Host "🚀 Starting AI Air Quality Agent with Gemini Integration" -ForegroundColor Green
Write-Host "=========================================================" -ForegroundColor White

# Check if Gemini API is configured
$envFile = "e:\Agent\ai-air-quality-agent\backend\.env"
if (Test-Path $envFile) {
    $envContent = Get-Content $envFile -Raw
    if ($envContent -match "GEMINI_API_KEY=(.+)") {
        Write-Host "✅ Gemini API key found" -ForegroundColor Green
    } else {
        Write-Host "❌ No Gemini API key found in .env file" -ForegroundColor Red
        Write-Host "   Please add GEMINI_API_KEY=your_key_here to $envFile" -ForegroundColor Yellow
        exit
    }
} else {
    Write-Host "❌ .env file not found at $envFile" -ForegroundColor Red
    exit
}

# Start backend server
Write-Host "`n📡 Starting Backend Server..." -ForegroundColor Cyan
$backendPath = "e:\Agent\ai-air-quality-agent\backend"
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$backendPath'; python -m uvicorn main:app --reload --port 8000" -WindowStyle Normal

# Wait for backend to start
Write-Host "⌛ Waiting for backend to initialize..." -ForegroundColor Yellow
Start-Sleep -Seconds 3

# Test backend health
try {
    $healthCheck = Invoke-RestMethod -Uri "http://localhost:8000/health" -Method Get -ErrorAction Stop
    Write-Host "✅ Backend server is running" -ForegroundColor Green
} catch {
    Write-Host "❌ Backend server failed to start properly" -ForegroundColor Red
    Write-Host "   Error: $_" -ForegroundColor Red
    exit
}

# Start frontend
Write-Host "`n🌐 Starting Frontend Server..." -ForegroundColor Cyan
$frontendPath = "e:\Agent\ai-air-quality-agent\frontend"
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$frontendPath'; npm start" -WindowStyle Normal

# Final instructions
Write-Host "`n✨ System Started Successfully!" -ForegroundColor Green
Write-Host "   Backend API: http://localhost:8000" -ForegroundColor White
Write-Host "   Frontend UI: http://localhost:3000" -ForegroundColor White
Write-Host "   API Docs: http://localhost:8000/docs" -ForegroundColor White

Write-Host "`n💡 Example queries:" -ForegroundColor Yellow
Write-Host "   - Show me average temperature in each room" -ForegroundColor White
Write-Host "   - Which room has the highest CO2 levels?" -ForegroundColor White
Write-Host "   - How does humidity vary throughout the day?" -ForegroundColor White

Write-Host "`nPress any key to exit this startup script..." -ForegroundColor Cyan
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
