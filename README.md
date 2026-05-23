# 计算机配件兼容性测试平台

毕业设计项目 - 硬件兼容性检测系统（Java + Python 双版本）

## 项目结构

`
├── 计算机配件兼容性测试平台-python版/    # Python版（FastAPI）
├── 项目源码/                              # Java版（Spring Boot）
└── 项目展示视频/
`

---

## Python版（FastAPI）

### 特点
- **零依赖**：仅3个外部依赖（fastapi、uvicorn、python-multipart）
- **标准库替代**：bcrypt->hashlib，pyjwt->hmac，psutil->ctypes+os
- **跨平台**：Windows / Linux / macOS 均可运行
- **内置功能**：认证、兼容性检测、系统监控、诊断与自修复

### 快速启动

`ash
# Windows
cd 计算机配件兼容性测试平台-python版
start.bat

# Linux/macOS
cd 计算机配件兼容性测试平台-python版
chmod +x start.sh
./start.sh
`

### 功能模块

| 模块 | 路径 | 说明 |
|------|------|------|
| 认证 | /api/auth/login | JWT登录/注册 |
| 配件库 | /api/compatibility/products | 133款近10年主流硬件配件 |
| 兼容性检测 | /api/compatibility/check | 多配件兼容性分析 |
| 系统监控 | /api/monitoring/dashboard | CPU/内存/磁盘/网络实时监控 |
| 诊断报告 | /api/diagnostics/report | 26个错误码，自动诊断 |
| 错误码手册 | /api/diagnostics/error-catalog | 错误码分类查询 |
| 自修复 | /api/diagnostics/fix/{code} | 自动修复可处理的问题 |

### 技术栈
- **后端**：Python 3.9+ / FastAPI / Uvicorn
- **前端**：Vue 3 / 暗黑风格 / 离线化
- **安全**：PBKDF2密码哈希 / HS256 JWT
- **监控**：跨平台系统信息采集

---

## Java版（Spring Boot）

### 特点
- 基于 Spring Boot 2.7 + Spring Security
- H2 嵌入式数据库，零配置运行
- JWT认证 + Swagger API文档
- 完整监控系统和错误码手册

### 快速启动

`ash
# Windows
cd 项目源码
ONE_CLICK_START.bat

# Linux/macOS
cd 项目源码
chmod +x ONE_CLICK_START.sh
./ONE_CLICK_START.sh
`

---

## 默认账号

| 用户名 | 密码 |
|--------|------|
| demo | 123456 |

---

## 依赖列表（Python版）

`
fastapi>=0.104.1,<1.0.0
uvicorn[standard]>=0.24.0,<1.0.0
python-multipart>=0.0.6,<1.0.0
`

## 依赖列表（Java版）

- Java 17+
- Maven 3.8+

---

## 作者

毕业设计项目
