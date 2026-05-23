@echo off
chcp 65001 >nul 2>&1
echo.
echo ============================================================
echo   Hardware Compatibility Platform - Quick Start
echo ============================================================
echo.
echo   1. Start full system (backend + frontend)
echo   2. Start backend only
echo   3. Open frontend only
echo   4. Check system status
echo.

set /p choice="Please select (1-4): "

if "%choice%"=="1" (
    echo Starting full system...
    call "%~dp0start-full-system.bat"
) else if "%choice%"=="2" (
    echo Starting backend...
    where java >nul 2>&1
    if %errorlevel% neq 0 (
        echo ERROR: Java not found. Please install JDK 17+.
        goto :end
    )
    where mvn >nul 2>&1
    if %errorlevel% neq 0 (
        echo ERROR: Maven not found. Please install Maven.
        goto :end
    )
    start "HardwareBackend" cmd /c "cd /d "%~dp0backend" && mvn spring-boot:run"
    echo Backend started on http://localhost:8080
) else if "%choice%"=="3" (
    echo Opening frontend...
    start "" "%~dp0frontend-simple\index.html"
) else if "%choice%"=="4" (
    echo Checking system status...
    powershell -NoProfile -Command "try { $r=Invoke-WebRequest -Uri 'http://localhost:8080/actuator/health' -UseBasicParsing -TimeoutSec 5; Write-Host 'Backend: UP (' $r.StatusCode ')' } catch { Write-Host 'Backend: DOWN' }" 2>nul
    echo Frontend: %~dp0frontend-simple\index.html
    if exist "%~dp0frontend-simple\index.html" (
        echo Frontend file: EXISTS
    ) else (
        echo Frontend file: MISSING
    )
) else (
    echo Invalid choice.
)

echo.
pause