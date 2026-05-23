#!/usr/bin/env bash
set -e

PROJECT_DIR=$(cd "$(dirname "$0")" && pwd)
TOOLS_DIR="$PROJECT_DIR/.tools"
JAVA_DIR="$TOOLS_DIR/jdk-17"
MAVEN_DIR="$TOOLS_DIR/maven"
JAVA_EXE="$JAVA_DIR/bin/java"
MVN_EXE="$MAVEN_DIR/bin/mvn"

echo ""
echo "============================================================"
echo "  Hardware Compatibility Platform - One-Click Launcher"
echo "============================================================"
echo ""
echo "  Auto-detect and install: JDK 17 + Maven"
echo "  No pre-installation required. Downloads automatically on first run."
echo "============================================================"
echo ""

# --------------------------
# Step 1: Detect OS and Architecture
# --------------------------
OS=$(uname -s)
ARCH=$(uname -m)
echo "[STEP 1/3] Detecting system..."

case "$OS" in
    Linux)
        if [ "$ARCH" = "x86_64" ]; then
            JDK_URL="https://github.com/adoptium/temurin17-binaries/releases/download/jdk-17.0.12%2B7/OpenJDK17U-jdk_x64_linux_hotspot_17.0.12_7.tar.gz"
        elif [ "$ARCH" = "aarch64" ]; then
            JDK_URL="https://github.com/adoptium/temurin17-binaries/releases/download/jdk-17.0.12%2B7/OpenJDK17U-jdk_aarch64_linux_hotspot_17.0.12_7.tar.gz"
        else
            echo "  [ERROR] Unsupported Linux architecture: $ARCH"
            exit 1
        fi
        ;;
    Darwin)
        if [ "$ARCH" = "x86_64" ]; then
            JDK_URL="https://github.com/adoptium/temurin17-binaries/releases/download/jdk-17.0.12%2B7/OpenJDK17U-jdk_x64_mac_hotspot_17.0.12_7.tar.gz"
        elif [ "$ARCH" = "arm64" ]; then
            JDK_URL="https://github.com/adoptium/temurin17-binaries/releases/download/jdk-17.0.12%2B7/OpenJDK17U-jdk_aarch64_mac_hotspot_17.0.12_7.tar.gz"
        else
            echo "  [ERROR] Unsupported macOS architecture: $ARCH"
            exit 1
        fi
        ;;
    *)
        echo "  [ERROR] Unsupported OS: $OS"
        exit 1
        ;;
esac

echo "  OS: $OS | Architecture: $ARCH"

# --------------------------
# Step 2: Check Java 17
# --------------------------
echo "[STEP 2/3] Checking Java 17..."
JAVA_OK=0

if [ -f "$JAVA_EXE" ]; then
    JAVA_VER=$("$JAVA_EXE" -version 2>&1 | head -1 | cut -d'"' -f2 | cut -d'.' -f1)
    if [ "$JAVA_VER" -ge 17 ] 2>/dev/null; then
        JAVA_OK=1
        echo "  [OK] Local JDK 17 found"
    fi
fi

if [ $JAVA_OK -eq 0 ]; then
    echo "  [DOWNLOAD] Downloading JDK 17..."
    mkdir -p "$TOOLS_DIR"
    
    if command -v wget &>/dev/null; then
        wget -q "$JDK_URL" -O "$TOOLS_DIR/jdk.tar.gz"
    elif command -v curl &>/dev/null; then
        curl -s -L "$JDK_URL" -o "$TOOLS_DIR/jdk.tar.gz"
    else
        echo "  [ERROR] Neither wget nor curl found. Please install one."
        exit 1
    fi
    
    echo "  [UNPACK] Extracting JDK..."
    tar -xzf "$TOOLS_DIR/jdk.tar.gz" -C "$TOOLS_DIR"
    mv "$TOOLS_DIR/jdk-17.0.12+7" "$JAVA_DIR"
    rm "$TOOLS_DIR/jdk.tar.gz"
    
    echo "  [OK] JDK 17 installed"
    JAVA_OK=1
fi

# --------------------------
# Step 3: Check Maven
# --------------------------
echo "[STEP 3/3] Checking Maven..."
MAVEN_OK=0

if [ -f "$MVN_EXE" ]; then
    MAVEN_OK=1
    echo "  [OK] Local Maven found"
fi

if [ $MAVEN_OK -eq 0 ]; then
    echo "  [DOWNLOAD] Downloading Maven..."
    
    MAVEN_URL="https://dlcdn.apache.org/maven/maven-3/3.9.6/binaries/apache-maven-3.9.6-bin.tar.gz"
    
    if command -v wget &>/dev/null; then
        wget -q "$MAVEN_URL" -O "$TOOLS_DIR/maven.tar.gz"
    else
        curl -s -L "$MAVEN_URL" -o "$TOOLS_DIR/maven.tar.gz"
    fi
    
    echo "  [UNPACK] Extracting Maven..."
    tar -xzf "$TOOLS_DIR/maven.tar.gz" -C "$TOOLS_DIR"
    mv "$TOOLS_DIR/apache-maven-3.9.6" "$MAVEN_DIR"
    rm "$TOOLS_DIR/maven.tar.gz"
    
    echo "  [OK] Maven installed"
    MAVEN_OK=1
fi

# --------------------------
# Step 4: Start Application
# --------------------------
echo ""
echo "[LAUNCH] Starting application..."
mkdir -p "$PROJECT_DIR/backend/data"

# Start backend in background
echo "  Starting backend server..."
cd "$PROJECT_DIR/backend"
"$MVN_EXE" spring-boot:run &
BACKEND_PID=$!
cd "$PROJECT_DIR"

# Wait for backend
echo "  Waiting for backend initialization..."
sleep 12

# Open frontend
echo "  Opening frontend..."
if command -v xdg-open &>/dev/null; then
    xdg-open "$PROJECT_DIR/frontend-simple/index.html"
elif command -v open &>/dev/null; then
    open "$PROJECT_DIR/frontend-simple/index.html"
else
    echo "  [INFO] Please open manually: $PROJECT_DIR/frontend-simple/index.html"
fi

echo ""
echo "============================================================"
echo "  System launched successfully!"
echo "============================================================"
echo ""
echo "  Backend API:    http://localhost:8080"
echo "  Frontend:       $PROJECT_DIR/frontend-simple/index.html"
echo ""
echo "  Username: demo   Password: 123456"
echo ""
echo "  First launch may take several minutes to download dependencies..."
echo "============================================================"

# Keep script running
wait $BACKEND_PID