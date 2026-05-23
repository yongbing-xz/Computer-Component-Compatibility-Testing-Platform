#!/usr/bin/env bash
# Hardware Compatibility Platform - Cross-platform Launcher
# Works on: Linux, macOS, Windows Git Bash, WSL
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
BACKEND_DIR="$SCRIPT_DIR/backend"
FRONTEND_DIR="$SCRIPT_DIR/frontend-simple"

echo ""
echo "============================================================"
echo "  Hardware Compatibility Platform - Full System Launcher"
echo "============================================================"
echo ""

# ---- Check dependencies ----
HAS_JAVA=false
HAS_MVN=false

if command -v java &>/dev/null; then
    HAS_JAVA=true
    JAVA_VER=$(java -version 2>&1 | head -1 | cut -d'"' -f2 | cut -d'.' -f1)
    if [ "$JAVA_VER" -lt 17 ] 2>/dev/null; then
        echo "[WARNING] Java $JAVA_VER detected. JDK 17+ is recommended."
    fi
else
    echo "[WARNING] Java not found. Backend will not start."
fi

if command -v mvn &>/dev/null; then
    HAS_MVN=true
elif command -v mvnw &>/dev/null; then
    HAS_MVN=true
    alias mvn='./mvnw'
elif [ -f "$BACKEND_DIR/target/compatibility-checker-1.0.0.jar" ]; then
    HAS_MVN=true
    echo "Pre-built JAR detected, will run directly."
else
    echo "[WARNING] Maven not found and no pre-built JAR."
fi

# ---- Create data directory ----
mkdir -p "$BACKEND_DIR/data" 2>/dev/null

# ---- Start Backend ----
if $HAS_JAVA && $HAS_MVN; then
    echo "[1/2] Starting backend (port ${SERVER_PORT:-8080})..."
    cd "$BACKEND_DIR"
    if [ -f "target/compatibility-checker-1.0.0.jar" ]; then
        java -jar target/compatibility-checker-1.0.0.jar &
    else
        mvn spring-boot:run &
    fi
    cd "$SCRIPT_DIR"
    echo "      Waiting for Spring Boot to initialize..."
    sleep 8
else
    echo "[SKIP] Backend environment not met."
fi

# ---- Start Frontend ----
echo "[2/2] Opening frontend..."

# Try different methods to open the HTML file
if command -v xdg-open &>/dev/null; then
    xdg-open "$FRONTEND_DIR/index.html"
elif command -v open &>/dev/null; then
    open "$FRONTEND_DIR/index.html"
elif command -v start &>/dev/null; then
    start "" "$FRONTEND_DIR/index.html"
else
    echo "      Open manually: $FRONTEND_DIR/index.html"
fi

echo ""
echo "============================================================"
echo "  System launched!"
echo "============================================================"
echo ""
echo "  Backend API:    http://localhost:${SERVER_PORT:-8080}"
echo "  Frontend:       $FRONTEND_DIR/index.html"
echo ""
echo "  Username: demo   Password: 123456"
echo "============================================================"