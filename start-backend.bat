@echo off
title VISIONARY API - Local Development Backend Launcher
color 0A

echo ======================================================================
echo           VISIONARY API - HE THONG QUAN LY HOAT DONG HOI NHAP
echo                       LOCAL DEVELOPMENT SERVER
echo ======================================================================
echo.

cd /d "%~dp0"

echo [1/1] Dang khoi dong ASP.NET Core 8 Web API tren cong localhost:5000...
echo - Swagger Documentation: http://localhost:5000/swagger
echo - Health Endpoint:       http://localhost:5000/health/live
echo.
echo Luu y: He thong production van hanh doc lap 24/7 tren Cloud (Render + Supabase).
echo File nay chi su dung de lap trinh va kiem thu cuc bo tren may ca nhan.
echo.

dotnet run --project backend/src/Visionary.Api/Visionary.Api.csproj --urls http://127.0.0.1:5000
