import os
import sys
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.auth import router as auth_router
from app.compatibility import router as compatibility_router
from app.monitoring import router as monitoring_router
from app.diagnostics import router as diagnostics_router
from app.config import DATA_DIR, JWT_KEY_FILE, settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用启动/关闭生命周期"""
    # 启动时确保必要目录和文件存在
    os.makedirs(DATA_DIR, exist_ok=True)
    # 触发JWT密钥生成（如果不存在）
    _ = settings.JWT_SECRET_KEY
    print(f"[启动] 数据目录: {DATA_DIR}")
    print(f"[启动] 服务运行在 http://{settings.HOST}:{settings.PORT}")
    yield


app = FastAPI(
    title="硬件兼容性检测系统",
    description="Hardware Compatibility Detection System - Python FastAPI Backend",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS配置 - 允许前端访问
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 挂载所有路由
app.include_router(auth_router)
app.include_router(compatibility_router)
app.include_router(monitoring_router)
app.include_router(diagnostics_router)

# 前端静态文件目录（Python版自带frontend）
_FRONTEND_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "frontend",
)


@app.get("/")
async def serve_index():
    index_path = os.path.join(_FRONTEND_DIR, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path, media_type="text/html; charset=utf-8")
    return {"message": "硬件兼容性检测系统 API", "docs": "/docs"}


# 静态文件服务（前端资源）- 带容错
_ASSETS_DIR = os.path.join(_FRONTEND_DIR, "assets")
_VENDOR_DIR = os.path.join(_FRONTEND_DIR, "vendor")

if os.path.isdir(_ASSETS_DIR):
    app.mount("/assets", StaticFiles(directory=_ASSETS_DIR), name="assets")
if os.path.isdir(_VENDOR_DIR):
    app.mount("/vendor", StaticFiles(directory=_VENDOR_DIR), name="vendor")


# 前端页面路由 - 自动扫描frontend目录下的文件
_MEDIA_TYPES = {
    "html": "text/html; charset=utf-8",
    "js": "application/javascript; charset=utf-8",
    "css": "text/css; charset=utf-8",
    "json": "application/json; charset=utf-8",
    "ico": "image/x-icon",
    "png": "image/png",
    "svg": "image/svg+xml",
}

# 需要注册路由的根级前端文件
_FRONTEND_FILES = [
    "login.html", "app.js", "styles.css", "products-data.js",
    "components.json", "favicon.ico",
]


def _register_frontend_routes():
    """注册前端静态文件路由，文件不存在则跳过"""
    if not os.path.isdir(_FRONTEND_DIR):
        print(f"[警告] 前端目录不存在: {_FRONTEND_DIR}，仅API模式运行")
        return

    for fname in _FRONTEND_FILES:
        fpath = os.path.join(_FRONTEND_DIR, fname)
        if not os.path.exists(fpath):
            continue
        ext = fname.rsplit(".", 1)[-1].lower()
        mt = _MEDIA_TYPES.get(ext, "application/octet-stream")

        def _make_handler(fp=fpath, media_type=mt):
            async def _handler():
                return FileResponse(fp, media_type=media_type)
            return _handler

        app.add_api_route(f"/{fname}", _make_handler(), methods=["GET"])


_register_frontend_routes()


@app.get("/api")
async def api_root():
    return {
        "service": "Hardware Compatibility Detection System",
        "version": "1.0.0",
        "python": sys.version,
        "platform": sys.platform,
        "endpoints": {
            "auth": "/api/auth",
            "compatibility": "/api/compatibility",
            "monitoring": "/api/monitoring",
            "diagnostics": "/api/diagnostics",
        },
    }
