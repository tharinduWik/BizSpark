Write-Host "🚀 Starting AI Air Quality Agent..." -ForegroundColor Green
Write-Host ""

Write-Host "📊 Starting Backend Server..." -ForegroundColor Blue
Set-Location "e:\Agent\ai-air-quality-agent\backend"
Start-Process PowerShell -ArgumentList "-NoExit", "-Command", "python -m uvicorn main:app --reload --port 8000" -WindowStyle Normal

Write-Host ""
Write-Host "⏳ Waiting 5 seconds for backend to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

Write-Host "🌐 Starting Frontend..." -ForegroundColor Blue
Set-Location "e:\Agent\ai-air-quality-agent\frontend"
Start-Process PowerShell -ArgumentList "-NoExit", "-Command", "npm start" -WindowStyle Normal

Write-Host ""
Write-Host "✅ Both servers are starting..." -ForegroundColor Green
Write-Host "🔗 Backend: http://localhost:8000" -ForegroundColor Cyan
Write-Host "🔗 Frontend: http://localhost:3000" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press any key to continue..."
$Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown") | Out-Null
