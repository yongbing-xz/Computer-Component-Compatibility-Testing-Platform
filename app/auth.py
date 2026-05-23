import hashlib
import hmac
import base64
import json
import os
import time
from datetime import datetime, timedelta
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel

from app.config import settings

router = APIRouter(prefix="/api/auth", tags=["认证"])

security = HTTPBearer()

# 内存用户存储
_users_db: dict = {}


# ==================== 标准库实现JWT（替代pyjwt） ====================

def _b64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("utf-8")


def _b64url_decode(s: str) -> bytes:
    padding = 4 - len(s) % 4
    if padding != 4:
        s += "=" * padding
    return base64.urlsafe_b64decode(s)


def _jwt_encode(payload: dict, secret: str, algorithm: str = "HS256") -> str:
    header = {"alg": algorithm, "typ": "JWT"}
    header_b64 = _b64url_encode(json.dumps(header, separators=(",", ":")).encode("utf-8"))
    payload_b64 = _b64url_encode(json.dumps(payload, separators=(",", ":")).encode("utf-8"))
    signing_input = f"{header_b64}.{payload_b64}"
    signature = hmac.new(secret.encode("utf-8"), signing_input.encode("utf-8"), hashlib.sha256).digest()
    return f"{signing_input}.{_b64url_encode(signature)}"


def _jwt_decode(token: str, secret: str, algorithms: list = None) -> dict:
    if algorithms is None:
        algorithms = ["HS256"]
    parts = token.split(".")
    if len(parts) != 3:
        raise ValueError("Invalid token format")

    header_b64, payload_b64, signature_b64 = parts
    signing_input = f"{header_b64}.{payload_b64}"

    # 验证签名
    expected_sig = hmac.new(secret.encode("utf-8"), signing_input.encode("utf-8"), hashlib.sha256).digest()
    actual_sig = _b64url_decode(signature_b64)
    if not hmac.compare_digest(expected_sig, actual_sig):
        raise ValueError("Invalid signature")

    payload = json.loads(_b64url_decode(payload_b64))

    # 检查过期
    if "exp" in payload and payload["exp"] < time.time():
        raise ValueError("Token expired")

    return payload


# ==================== 标准库实现密码哈希（替代bcrypt） ====================

def _hash_password(password: str) -> str:
    """使用PBKDF2 + 随机盐值哈希密码"""
    salt = os.urandom(16)
    key = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 100000)
    return f"pbkdf2:sha256:100000${base64.b64encode(salt).decode()}${base64.b64encode(key).decode()}"


def _verify_password(password: str, hashed: str) -> bool:
    """验证密码是否匹配"""
    try:
        if not hashed.startswith("pbkdf2:"):
            return False
        parts = hashed.split("$")
        if len(parts) != 3:
            return False
        salt = base64.b64decode(parts[1])
        stored_key = base64.b64decode(parts[2])
        new_key = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 100000)
        return hmac.compare_digest(stored_key, new_key)
    except Exception:
        return False


# ==================== 数据模型 ====================

class LoginRequest(BaseModel):
    username: str
    password: str


class RegisterRequest(BaseModel):
    username: str
    password: str
    email: Optional[str] = None


class TokenResponse(BaseModel):
    token: str
    type: str = "Bearer"
    expiresIn: int


class UserInfo(BaseModel):
    id: int
    username: str
    email: Optional[str] = None
    role: str = "user"


# ==================== 初始化 ====================

def _init_demo_user():
    if settings.DEMO_USER not in _users_db:
        _users_db[settings.DEMO_USER] = {
            "id": 1,
            "username": settings.DEMO_USER,
            "password": _hash_password(settings.DEMO_PASSWORD),
            "email": "demo@example.com",
            "role": "admin",
        }


_init_demo_user()


def create_access_token(username: str) -> str:
    expire = time.time() + settings.JWT_EXPIRE_HOURS * 3600
    payload = {"sub": username, "exp": expire, "iat": time.time()}
    return _jwt_encode(payload, settings.JWT_SECRET_KEY)


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    token = credentials.credentials
    try:
        payload = _jwt_decode(token, settings.JWT_SECRET_KEY)
        username: str = payload.get("sub")
        if username is None or username not in _users_db:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="无效的认证凭据")
        return _users_db[username]
    except ValueError as e:
        if "expired" in str(e).lower():
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token已过期")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="无效的Token")


@router.post("/login", response_model=TokenResponse)
async def login(req: LoginRequest):
    user = _users_db.get(req.username)
    if not user or not _verify_password(req.password, user["password"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="用户名或密码错误")
    token = create_access_token(req.username)
    return TokenResponse(token=token, expiresIn=settings.JWT_EXPIRE_HOURS * 3600)


@router.post("/register")
async def register(req: RegisterRequest):
    if req.username in _users_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="用户名已存在")
    user_id = len(_users_db) + 1
    _users_db[req.username] = {
        "id": user_id,
        "username": req.username,
        "password": _hash_password(req.password),
        "email": req.email,
        "role": "user",
    }
    token = create_access_token(req.username)
    return {"message": "注册成功", "token": token, "type": "Bearer", "expiresIn": settings.JWT_EXPIRE_HOURS * 3600}


@router.get("/me", response_model=UserInfo)
async def get_me(user: dict = Depends(get_current_user)):
    return UserInfo(
        id=user["id"],
        username=user["username"],
        email=user.get("email"),
        role=user.get("role", "user"),
    )
