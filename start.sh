#!/usr/bin/env bash
set -e

SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)
cd "$SCRIPT_DIR"

echo ""
echo "============================================================"
echo "  硬件兼容性检测系统 - Python FastAPI 后端"
echo "============================================================"
echo ""

# ========== 1. 检测Python ==========
PYTHON=""
if command -v python3 &>/dev/null; then
    PYTHON=python3
elif command -v python &>/dev/null; then
    PYTHON=python
fi

if [ -z "$PYTHON" ]; then
    echo "[错误] 未检测到Python，请先安装 Python 3.9+"
    echo "  下载地址: https://www.python.org/downloads/"
    exit 1
fi

echo "[1/5] Python环境: $($PYTHON --version)"

# ========== 2. 检测Python版本 ==========
PY_VER=$($PYTHON --version 2>&1 | awk '{print $2}')
PY_MAJOR=$(echo "$PY_VER" | cut -d. -f1)
PY_MINOR=$(echo "$PY_VER" | cut -d. -f2)

if [ "$PY_MAJOR" -lt 3 ] || { [ "$PY_MAJOR" -eq 3 ] && [ "$PY_MINOR" -lt 9 ]; }; then
    echo "[错误] Python版本过低，需要3.9+，当前: $PY_VER"
    exit 1
fi
echo "Python版本检查通过: $PY_VER"

# ========== 3. 创建虚拟环境（可选） ==========
if [ ! -f "venv/bin/activate" ]; then
    echo "[2/5] 首次运行，创建虚拟环境..."
    $PYTHON -m venv venv || echo "[警告] 虚拟环境创建失败，将使用系统Python"
else
    echo "[2/5] 虚拟环境已存在"
fi

# 激活虚拟环境
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
    PYTHON=python
fi

# ========== 4. 安装依赖 ==========
echo "[3/5] 检查并安装依赖..."
pip install -r requirements.txt -q 2>/dev/null || {
    echo "[警告] 依赖安装可能不完整，尝试逐个安装..."
    pip install fastapi uvicorn python-multipart -q 2>/dev/null
}
echo "依赖检查完成"

# ========== 5. 检测端口冲突 ==========
PORT=8080
echo "[4/5] 检测端口 $PORT ..."

check_port() {
    if lsof -i ":$1" &>/dev/null; then
        return 0  # 端口被占用
    elif netstat -an 2>/dev/null | grep -q ":$1 .*LISTEN"; then
        return 0  # 端口被占用
    else
        return 1  # 端口可用
    fi
}

if check_port $PORT; then
    echo "[警告] 端口 $PORT 已被占用，尝试使用8081..."
    PORT=8081
    if check_port $PORT; then
        echo "[错误] 端口8080和8081均被占用，请手动释放端口"
        exit 1
    fi
fi
echo "端口 $PORT 可用"

# ========== 6. 确保数据目录存在 ==========
mkdir -p app/data

# ========== 7. 启动服务 ==========
echo "[5/5] 启动服务 (端口: $PORT)..."
$PYTHON -m uvicorn app.main:app --host 0.0.0.0 --port $PORT &
SERVER_PID=$!

# 等待服务启动
echo "等待服务启动..."
for i in $(seq 1 10); do
    if curl -s "http://localhost:$PORT/api/monitoring/health" &>/dev/null; then
        echo "服务启动成功！"
        break
    fi
    sleep 1
done

echo ""
echo "============================================================"
echo "  访问地址:  http://localhost:$PORT"
echo "  API文档:   http://localhost:$PORT/docs"
echo "  账号密码:  demo / 123456"
echo "============================================================"
echo ""

# 打开浏览器
if command -v xdg-open &>/dev/null; then
    xdg-open "http://localhost:$PORT"
elif command -v open &>/dev/null; then
    open "http://localhost:$PORT"
fi

# 等待服务进程
wait $SERVER_PID
