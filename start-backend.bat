@echo off
title VISIONARY API - Backend & Cloudflare Tunnel Launcher
color 0A

echo ======================================================================
echo           VISIONARY API - HE THONG QUAN LY HOAT DONG HOI NHAP
echo                       ONE BACKEND - THREE PLATFORMS
echo ======================================================================
echo.

cd /d "%~dp0"

echo [1/2] Dang khoi dong ASP.NET Core 8 Web API tren cong 5000...
start "Visionary Web API (Kestrel :5000)" dotnet run --project backend/src/Visionary.Api/Visionary.Api.csproj --urls http://0.0.0.0:5000

timeout /t 4 /nobreak >nul

echo [2/2] Dang khoi dong Cloudflare HTTPS Tunnel...
if exist "C:\Program Files (x86)\cloudflared\cloudflared.exe" (
    start "Cloudflare Tunnel" "C:\Program Files (x86)\cloudflared\cloudflared.exe" tunnel --url http://127.0.0.1:5000
) else (
    echo Khong tim thay cloudflared.exe tai C:\Program Files (x86)\cloudflared\
)

echo.
echo ======================================================================
echo [OK] Backend va Tunnel da duoc khoi chay ngam thanh cong!
echo - Website Vercel: https://visionary-platform.vercel.app
echo - Local API:      http://localhost:5000/swagger
echo ======================================================================
echo.
pause
