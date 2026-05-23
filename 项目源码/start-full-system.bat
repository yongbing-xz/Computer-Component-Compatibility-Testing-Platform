@echo off
chcp 65001 >nul 2>&1
setlocal enabledelayedexpansion

echo.
echo ============================================================
echo   Hardware Compatibility Platform - Full System Launcher
echo ============================================================
echo.

REM ---- 0. Locate project root ----
set "PROJECT_ROOT=%~dp0"
set "BACKEND_DIR=%PROJECT_ROOT%backend"
set "FRONTEND_DIR=%PROJECT_ROOT%frontend-simple"

REM Check Java
where java >nul 2>&1
if %errorlevel% neq 0 (
    echo [WARNING] Java not found in PATH. Please install JDK 17+.
    echo           后端将无法启动，前端仍可打开。
    set "SKIP_BACKEND=1"
)

REM Check Maven
where mvn >nul 2>&1
if %errorlevel% neq 0 (
    echo [WARNING] Maven not found in PATH.
    echo           如果 backend/target/ 下没有已编译的jar, 后端将无法启动。
    set "SKIP_BACKEND=1"
)

REM ---- 1. Start Backend ----
if defined SKIP_BACKEND (
    echo [SKIP] 后端环境不满足，跳过启动
    goto :start_frontend
)

echo [1/2] Starting backend (port 8080)...
start "HardwareBackend" cmd /c "cd /d "%BACKEND_DIR%" && mvn spring-boot:run"

REM Wait for backend to warm up (non-blocking)
echo         Waiting for Spring Boot to initialize...
powershell -NoProfile -Command "Start-Sleep -Seconds 8" >nul 2>&1

REM ---- 2. Start Frontend ----
:start_frontend
echo [2/2] Opening frontend...
start "" "%FRONTEND_DIR%\index.html"

echo.
echo ============================================================
echo   System launched!
echo ============================================================
echo.
echo   Backend API:    http://localhost:8080
echo   Frontend:       file:///%FRONTEND_DIR:\=/%index.html
echo.
echo   Username: demo   Password: 123456
echo.
echo ============================================================
pause