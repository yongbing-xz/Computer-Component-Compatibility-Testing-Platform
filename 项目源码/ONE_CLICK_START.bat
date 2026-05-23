@echo off
chcp 65001 >nul 2>&1
setlocal enabledelayedexpansion

set "PROJECT_DIR=%~dp0"
set "TOOLS_DIR=%PROJECT_DIR%.tools"
set "JAVA_DIR=%TOOLS_DIR%\jdk-17"
set "MAVEN_DIR=%TOOLS_DIR%\maven"
set "JAVA_EXE=%JAVA_DIR%\bin\java.exe"
set "MVN_EXE=%MAVEN_DIR%\bin\mvn.cmd"

echo.
echo ============================================================
echo   Hardware Compatibility Platform - One-Click Launcher
echo ============================================================
echo.
echo   自动检测并安装依赖：JDK 17 + Maven
echo   无需提前安装，首次运行自动下载（需联网）
echo ============================================================
echo.

REM --------------------------
REM Step 1: Check Java 17
REM --------------------------
echo [STEP 1/3] 检测 Java 17...
set "JAVA_OK=0"
if exist "%JAVA_EXE%" (
    for /f "tokens=3" %%g in ('"%JAVA_EXE%" -version 2^>&1 ^| findstr /i "version"') do (
        set "JAVA_VER=%%g"
        set "JAVA_VER=!JAVA_VER:"=!"
        for /f "delims=." %%v in ("!JAVA_VER!") do (
            if %%v geq 17 (
                set "JAVA_OK=1"
                echo         [OK] 本地 JDK 17 已就绪
            )
        )
    )
)

if %JAVA_OK% equ 0 (
    echo         [DOWNLOAD] 正在下载 JDK 17...
    mkdir "%TOOLS_DIR%" 2>nul
    
    REM 下载 JDK 17 (Adoptium Temurin)
    powershell -NoProfile -Command ^
        "Invoke-WebRequest -Uri 'https://github.com/adoptium/temurin17-binaries/releases/download/jdk-17.0.12%2B7/OpenJDK17U-jdk_x64_windows_hotspot_17.0.12_7.zip' -OutFile '%TOOLS_DIR%\jdk.zip' -UseBasicParsing"
    
    echo         [UNPACK] 解压 JDK...
    powershell -NoProfile -Command ^
        "Expand-Archive -Path '%TOOLS_DIR%\jdk.zip' -DestinationPath '%TOOLS_DIR%' -Force"
    
    REM 重命名目录
    for /d %%d in ("%TOOLS_DIR%\jdk-17*") do (
        ren "%%d" "jdk-17"
    )
    
    del "%TOOLS_DIR%\jdk.zip"
    echo         [OK] JDK 17 安装完成
    set "JAVA_OK=1"
)

REM --------------------------
REM Step 2: Check Maven
REM --------------------------
echo [STEP 2/3] 检测 Maven...
set "MAVEN_OK=0"
if exist "%MVN_EXE%" (
    set "MAVEN_OK=1"
    echo         [OK] 本地 Maven 已就绪
)

if %MAVEN_OK% equ 0 (
    echo         [DOWNLOAD] 正在下载 Maven...
    
    powershell -NoProfile -Command ^
        "Invoke-WebRequest -Uri 'https://dlcdn.apache.org/maven/maven-3/3.9.6/binaries/apache-maven-3.9.6-bin.zip' -OutFile '%TOOLS_DIR%\maven.zip' -UseBasicParsing"
    
    echo         [UNPACK] 解压 Maven...
    powershell -NoProfile -Command ^
        "Expand-Archive -Path '%TOOLS_DIR%\maven.zip' -DestinationPath '%TOOLS_DIR%' -Force"
    
    ren "%TOOLS_DIR%\apache-maven-3.9.6" "maven"
    del "%TOOLS_DIR%\maven.zip"
    echo         [OK] Maven 安装完成
    set "MAVEN_OK=1"
)

REM --------------------------
REM Step 3: Start Application
REM --------------------------
echo [STEP 3/3] 启动应用...

REM Ensure data directory exists
mkdir "%PROJECT_DIR%backend\data" 2>nul

REM Start backend
echo         启动后端服务...
start "HardwareBackend" cmd /c "cd /d ""%PROJECT_DIR%backend"" && ""%MVN_EXE%"" spring-boot:run"

REM Wait for backend
echo         等待后端初始化...
powershell -NoProfile -Command "Start-Sleep -Seconds 10"

REM Open frontend
echo         打开前端页面...
start "" "%PROJECT_DIR%frontend-simple\index.html"

echo.
echo ============================================================
echo   System launched successfully!
echo ============================================================
echo.
echo   Backend API:    http://localhost:8080
echo   Frontend:       %PROJECT_DIR%frontend-simple\index.html
echo.
echo   Username: demo   Password: 123456
echo.
echo   首次启动可能需要几分钟下载依赖，请耐心等待...
echo ============================================================
pause