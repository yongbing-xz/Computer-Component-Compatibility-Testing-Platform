@echo off
chcp 65001 >nul 2>&1
setlocal enabledelayedexpansion
title 硬件兼容性检测系统 - Python版

echo.
echo ============================================================
echo   硬件兼容性检测系统 - Python FastAPI 后端
echo ============================================================
echo.

:: 切换到脚本所在目录
cd /d "%~dp0"

:: ========== 1. 检测Python ==========
set "PYTHON="
where python >nul 2>&1
if %errorlevel% equ 0 (
    set "PYTHON=python"
) else (
    where python3 >nul 2>&1
    if %errorlevel% equ 0 (
        set "PYTHON=python3"
    )
)

if not defined PYTHON (
    echo [错误] 未检测到Python，请先安装 Python 3.9+
    echo 下载地址: https://www.python.org/downloads/
    echo 安装时请勾选 "Add Python to PATH"
    pause
    exit /b 1
)

echo [1/5] Python环境:
!PYTHON! --version
echo.

:: ========== 2. 检测Python版本 ==========
for /f "tokens=2 delims= " %%v in ('!PYTHON! --version 2^>^&1') do set "PY_VER=%%v"
for /f "tokens=1,2 delims=." %%a in ("!PY_VER!") do (
    set "PY_MAJOR=%%a"
    set "PY_MINOR=%%b"
)
if !PY_MAJOR! lss 3 (
    echo [错误] Python版本过低，需要3.9+，当前: !PY_VER!
    pause
    exit /b 1
)
if !PY_MAJOR! equ 3 if !PY_MINOR! lss 9 (
    echo [错误] Python版本过低，需要3.9+，当前: !PY_VER!
    pause
    exit /b 1
)
echo Python版本检查通过: !PY_VER!
echo.

:: ========== 3. 创建虚拟环境（可选） ==========
if not exist "venv\Scripts\activate.bat" (
    echo [2/5] 首次运行，创建虚拟环境...
    !PYTHON! -m venv venv
    if %errorlevel% neq 0 (
        echo [警告] 虚拟环境创建失败，将使用系统Python
    ) else (
        echo 虚拟环境创建成功
    )
) else (
    echo [2/5] 虚拟环境已存在
)

:: 激活虚拟环境
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
    set "PYTHON=python"
)
echo.

:: ========== 4. 安装依赖 ==========
echo [3/5] 检查并安装依赖...
pip install -r requirements.txt -q 2>nul
if %errorlevel% neq 0 (
    echo [警告] 依赖安装可能不完整，尝试逐个安装...
    pip install fastapi uvicorn python-multipart -q 2>nul
)
echo 依赖检查完成
echo.

:: ========== 5. 检测端口冲突 ==========
set "PORT=8080"
echo [4/5] 检测端口 !PORT! ...
netstat -ano | findstr ":!PORT! " | findstr "LISTENING" >nul 2>&1
if %errorlevel% equ 0 (
    echo [警告] 端口 !PORT! 已被占用，尝试释放...
    for /f "tokens=5" %%p in ('netstat -ano ^| findstr ":!PORT! " ^| findstr "LISTENING"') do (
        echo 正在终止占用进程 PID: %%p
        taskkill /PID %%p /F >nul 2>&1
    )
    timeout /t 2 /nobreak >nul
    netstat -ano | findstr ":!PORT! " | findstr "LISTENING" >nul 2>&1
    if %errorlevel% equ 0 (
        echo [警告] 端口 !PORT! 仍被占用，尝试使用8081...
        set "PORT=8081"
        netstat -ano | findstr ":!PORT! " | findstr "LISTENING" >nul 2>&1
        if %errorlevel% equ 0 (
            echo [错误] 端口8080和8081均被占用，请手动关闭占用进程
            pause
            exit /b 1
        )
    )
)
echo 端口 !PORT! 可用
echo.

:: ========== 6. 确保数据目录存在 ==========
if not exist "app\data" mkdir "app\data"

:: ========== 7. 启动服务 ==========
echo [5/5] 启动服务 (端口: !PORT!)...
echo.
start "" cmd /c "!PYTHON! -m uvicorn app.main:app --host 0.0.0.0 --port !PORT!"

:: 等待服务启动
timeout /t 4 /nobreak >nul

:: 检测服务是否启动成功
set "STARTED=0"
for /l %%i in (1,1,5) do (
    if !STARTED! equ 0 (
        !PYTHON! -c "import urllib.request; urllib.request.urlopen('http://localhost:!PORT!/api/monitoring/health', timeout=2)" >nul 2>&1
        if !errorlevel! equ 0 (
            set "STARTED=1"
        ) else (
            timeout /t 2 /nobreak >nul
        )
    )
)

echo.
echo ============================================================
if !STARTED! equ 1 (
    echo   服务启动成功！
) else (
    echo   服务可能正在启动中，请稍候访问...
)
echo ============================================================
echo.
echo   访问地址:  http://localhost:!PORT!
echo   API文档:   http://localhost:!PORT!/docs
echo   账号密码:  demo / 123456
echo.
echo   按 Ctrl+C 停止服务
echo ============================================================
echo.

:: 打开浏览器
start http://localhost:!PORT!

pause
