@echo off
chcp 65001 >nul 2>&1
echo.
echo ============================================================
echo   Hardware Compatibility Platform - System Status
echo ============================================================
echo.

REM ---- Backend ----
echo Backend Service:
powershell -NoProfile -Command "try { $r=Invoke-WebRequest -Uri 'http://localhost:8080/actuator/health' -UseBasicParsing -TimeoutSec 5; Write-Host '  [UP] Backend running (HTTP' $r.StatusCode ')' } catch { Write-Host '  [DOWN] Backend not running on port 8080' }" 2>nul

echo.

REM ---- Files ----
echo File Integrity:
if exist "%~dp0backend\pom.xml" ( echo   [OK] backend/pom.xml ) else ( echo   [MISS] backend/pom.xml )
if exist "%~dp0frontend-simple\index.html" ( echo   [OK] frontend-simple/index.html ) else ( echo   [MISS] frontend-simple/index.html )
if exist "%~dp0frontend-simple\products-data.js" ( echo   [OK] frontend-simple/products-data.js ) else ( echo   [MISS] frontend-simple/products-data.js )
if exist "%~dp0frontend-simple\vendor\vue.global.prod.js" ( echo   [OK] frontend-simple/vendor/vue.global.prod.js (offline support) ) else ( echo   [WARN] Vue.js vendor file missing (online CDN fallback) )

echo.
echo ============================================================
echo   Quick Actions:
echo     start-full-system.bat  - Launch everything
echo     quick-start.bat        - Interactive menu
echo.
echo   Default Login: demo / 123456
echo ============================================================
echo.
pause