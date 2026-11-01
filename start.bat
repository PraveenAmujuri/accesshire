@echo off
REM AccessHire AI - One-Command Startup Script for Windows CMD
echo ==========================================================
echo          Starting AccessHire AI Platform...
echo ==========================================================

set ROOT_DIR=%~dp0

echo [1/3] Starting FastAPI Backend on http://127.0.0.1:8000...
start "AccessHire - Backend (Port 8000)" cmd /k "cd /d "%ROOT_DIR%backend" && .venv\Scripts\uvicorn.exe app.main:app --host 127.0.0.1 --port 8000 --reload"

echo [2/3] Starting Marketing Frontend on http://127.0.0.1:5173...
start "AccessHire - Marketing (Port 5173)" cmd /k "cd /d "%ROOT_DIR%frontend-marketing" && npm run dev -- --host 127.0.0.1 --port 5173"

echo [3/3] Starting Interview Frontend on http://127.0.0.1:5174...
start "AccessHire - Interview (Port 5174)" cmd /k "cd /d "%ROOT_DIR%frontend-interview" && npm run dev -- --host 127.0.0.1 --port 5174"

echo.
echo All services launched in dedicated windows:
echo   - Marketing Site:   http://127.0.0.1:5173
echo   - Interview Room:   http://127.0.0.1:5174
echo   - Backend API Docs: http://127.0.0.1:8000/docs
echo ==========================================================
