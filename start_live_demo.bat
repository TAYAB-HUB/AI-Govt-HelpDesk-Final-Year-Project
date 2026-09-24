@echo off
title AI Govt Helpdesk - Live Demo Launcher
echo ========================================================
echo    Starting AI Govt Helpdesk Backend and Live Tunnel...
echo ========================================================
echo.

cd /d "%~dp0backend"
echo [1/2] Starting FastAPI Backend on port 8001...
start "AI Helpdesk Backend" /min ..\.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8001

timeout /t 3 /nobreak >nul

echo [2/2] Starting Cloudflare HTTPS Tunnel...
echo.
echo ========================================================
echo Keep this window OPEN while testing your Vercel website!
echo Look below for your live trycloudflare.com HTTPS URL:
echo ========================================================
echo.
cloudflared.exe tunnel --url http://127.0.0.1:8001
pause
