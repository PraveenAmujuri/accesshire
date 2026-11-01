# AccessHire AI - One-Command Startup Script for PowerShell
# Launches Backend (FastAPI :8000), Marketing Frontend (:5173), and Interview Workspace (:5174)

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "         Starting AccessHire AI Platform...               " -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

$RootDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# 1. Start FastAPI Backend (:8000)
Write-Host "[1/3] Starting FastAPI Backend on http://127.0.0.1:8000..." -ForegroundColor Yellow
$BackendProc = Start-Process powershell -ArgumentList "-NoExit", "-Command", "Set-Location '$RootDir\backend'; & '.\.venv\Scripts\uvicorn.exe' app.main:app --host 127.0.0.1 --port 8000 --reload" -PassThru

# 2. Start Marketing Frontend (:5173)
Write-Host "[2/3] Starting Marketing Frontend on http://127.0.0.1:5173..." -ForegroundColor Yellow
$MarketingProc = Start-Process powershell -ArgumentList "-NoExit", "-Command", "Set-Location '$RootDir\frontend-marketing'; npm run dev -- --host 127.0.0.1 --port 5173" -PassThru

# 3. Start Interview Workspace (:5174)
Write-Host "[3/3] Starting Interview Frontend on http://127.0.0.1:5174..." -ForegroundColor Yellow
$InterviewProc = Start-Process powershell -ArgumentList "-NoExit", "-Command", "Set-Location '$RootDir\frontend-interview'; npm run dev -- --host 127.0.0.1 --port 5174" -PassThru

Write-Host ""
Write-Host "AccessHire AI services are now running in separate windows:" -ForegroundColor Green
Write-Host "  - Marketing Site:   http://127.0.0.1:5173" -ForegroundColor White
Write-Host "  - Interview Room:   http://127.0.0.1:5174" -ForegroundColor White
Write-Host "  - Backend API Docs: http://127.0.0.1:8000/docs" -ForegroundColor White
Write-Host "==========================================================" -ForegroundColor Cyan
