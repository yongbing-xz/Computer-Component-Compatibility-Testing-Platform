import glob
import os
import sys
import time
from typing import Optional

from fastapi import APIRouter
from pydantic import BaseModel

from app.config import settings, DATA_DIR, JWT_KEY_FILE
from app.monitoring import _get_cpu_info, _get_memory_info, _get_disk_info

router = APIRouter(prefix="/api/diagnostics", tags=["诊断与修复"])


# ==================== 错误码定义（26个，7大分类） ====================
class ErrorCode:
    # ---- CPU 相关 (HC-1001 ~ HC-1004) ----
    HC_1001 = ("HC-1001", "CPU_OVERHEAT", "critical", "CPU温度过高",
               "CPU温度超过安全阈值(90°C)，可能导致降频或自动关机", "检查散热器安装、更换硅脂、增强机箱风道")
    HC_1002 = ("HC-1002", "CPU_HIGH_USAGE", "warning", "CPU使用率过高",
               "CPU持续使用率超过90%，系统响应可能变慢", "关闭不必要的后台程序、检查是否有恶意进程")
    HC_1003 = ("HC-1003", "CPU_SOCKET_MISMATCH", "critical", "CPU接口不匹配",
               "CPU接口与主板CPU插槽不兼容", "更换匹配接口的CPU或主板")
    HC_1004 = ("HC-1004", "CPU_TDP_EXCEED", "warning", "CPU功耗超限",
               "CPU TDP超过主板供电能力", "更换低功耗CPU或升级主板供电模块")

    # ---- 内存相关 (HC-2001 ~ HC-2004) ----
    HC_2001 = ("HC-2001", "MEMORY_HIGH_USAGE", "warning", "内存使用率过高",
               "内存使用率超过85%，系统可能开始使用虚拟内存", "关闭不必要的程序、增加物理内存")
    HC_2002 = ("HC-2002", "MEMORY_DDR_MISMATCH", "critical", "内存DDR类型不匹配",
               "内存DDR类型与主板内存插槽不兼容", "更换匹配DDR类型的内存条")
    HC_2003 = ("HC-2003", "MEMORY_INSUFFICIENT", "warning", "内存容量不足",
               "可用内存低于总量的10%", "增加内存条或优化内存使用")
    HC_2004 = ("HC-2004", "MEMORY_SPEED_MISMATCH", "info", "内存频率不匹配",
               "内存频率与主板支持频率不一致，将以较低频率运行", "更换匹配频率的内存或调整BIOS设置")

    # ---- 存储相关 (HC-3001 ~ HC-3004) ----
    HC_3001 = ("HC-3001", "DISK_HIGH_USAGE", "warning", "磁盘使用率过高",
               "磁盘使用率超过90%，可能影响系统性能", "清理不必要的文件、扩展存储空间")
    HC_3002 = ("HC-3002", "DISK_IO_HIGH", "warning", "磁盘IO负载过高",
               "磁盘IO等待时间过长", "减少磁盘密集型操作、考虑升级SSD")
    HC_3003 = ("HC-3003", "NVME_INTERFACE_MISMATCH", "critical", "NVMe接口不匹配",
               "NVMe固态硬盘接口与主板M.2插槽不兼容", "更换匹配接口的NVMe或主板")
    HC_3004 = ("HC-3004", "DISK_SPACE_LOW", "critical", "磁盘空间不足",
               "可用磁盘空间低于5GB", "立即清理磁盘空间")

    # ---- GPU相关 (HC-4001 ~ HC-4004) ----
    HC_4001 = ("HC-4001", "GPU_OVERHEAT", "critical", "显卡温度过高",
               "显卡温度超过安全阈值(85°C)", "检查显卡散热、增强机箱风道")
    HC_4002 = ("HC-4002", "GPU_LENGTH_EXCEED", "critical", "显卡长度超限",
               "显卡长度超过机箱显卡限长", "更换较短显卡或更大机箱")
    HC_4003 = ("HC-4003", "GPU_DRIVER_OUTDATED", "info", "显卡驱动过旧",
               "显卡驱动版本较旧，可能影响性能和兼容性", "更新显卡驱动到最新版本")
    HC_4004 = ("HC-4004", "GPU_POWER_INSUFFICIENT", "warning", "显卡供电不足",
               "电源功率可能不足以支撑显卡满载运行", "更换更大功率电源")

    # ---- 系统相关 (HC-5001 ~ HC-5005) ----
    HC_5001 = ("HC-5001", "SYSTEM_HIGH_LOAD", "warning", "系统负载过高",
               "系统平均负载超过CPU核心数的2倍", "检查系统进程、优化资源使用")
    HC_5002 = ("HC-5002", "SYSTEM_PROCESS_TOO_MANY", "info", "系统进程数过多",
               "运行中的进程数超过500", "关闭不必要的后台进程")
    HC_5003 = ("HC-5003", "SYSTEM_UPTIME_LONG", "info", "系统运行时间过长",
               "系统已连续运行超过30天，建议重启", "安排系统重启以释放资源")
    HC_5004 = ("HC-5004", "SYSTEM_SWAP_HIGH", "warning", "交换空间使用过高",
               "交换空间使用率超过50%", "增加物理内存或调整swap配置")
    HC_5005 = ("HC-5005", "SYSTEM_NETWORK_ERROR", "warning", "网络异常",
               "网络丢包率过高或连接异常", "检查网络连接、DNS配置")

    # ---- 兼容性相关 (HC-6001 ~ HC-6003) ----
    HC_6001 = ("HC-6001", "COMPAT_CPU_MOTHERBOARD", "critical", "CPU与主板不兼容",
               "CPU接口与主板CPU插槽不匹配", "更换匹配的CPU或主板")
    HC_6002 = ("HC-6002", "COMPAT_MEMORY_MOTHERBOARD", "critical", "内存与主板不兼容",
               "内存DDR类型与主板内存插槽不匹配", "更换匹配DDR类型的内存条")
    HC_6003 = ("HC-6003", "COMPAT_GPU_CHASSIS", "critical", "显卡与机箱不兼容",
               "显卡长度超过机箱显卡限长", "更换较短显卡或更大机箱")

    # ---- 服务相关 (HC-7001 ~ HC-7002) ----
    HC_7001 = ("HC-7001", "SERVICE_JWT_EXPIRED", "warning", "JWT密钥过期",
               "JWT密钥可能已失效或不安全", "重新生成JWT密钥")
    HC_7002 = ("HC-7002", "SERVICE_DIR_MISSING", "warning", "必要目录缺失",
               "系统运行所需的目录不存在", "自动创建缺失目录")


# 错误码注册表
ERROR_CATALOG = {}
_all_error_attrs = [attr for attr in dir(ErrorCode) if attr.startswith("HC_")]
for _attr in _all_error_attrs:
    _val = getattr(ErrorCode, _attr)
    ERROR_CATALOG[_val[0]] = {
        "code": _val[0],
        "name": _val[1],
        "severity": _val[2],
        "title": _val[3],
        "description": _val[4],
        "solution": _val[5],
        "category": _val[0].split("-")[1][0] + "000",
    }

CATEGORY_MAP = {
    "1000": "CPU相关",
    "2000": "内存相关",
    "3000": "存储相关",
    "4000": "GPU相关",
    "5000": "系统相关",
    "6000": "兼容性相关",
    "7000": "服务相关",
}


class FixResult(BaseModel):
    code: str
    success: bool
    message: str
    details: Optional[str] = None


def _run_diagnostics() -> list[dict]:
    """执行实时诊断，返回当前检测到的问题列表"""
    found = []
    cpu_info = _get_cpu_info()
    mem_info = _get_memory_info()
    disk_info = _get_disk_info()

    if cpu_info["usage"] > 90:
        found.append(ERROR_CATALOG["HC-1002"])
    if mem_info["usagePercent"] > 85:
        found.append(ERROR_CATALOG["HC-2001"])
    if mem_info["usagePercent"] > 90:
        found.append(ERROR_CATALOG["HC-2003"])
    if disk_info["usagePercent"] > 90:
        found.append(ERROR_CATALOG["HC-3001"])
    if disk_info["free"] < 5 * 1024 * 1024 * 1024:
        found.append(ERROR_CATALOG["HC-3004"])

    # 服务相关
    if not os.path.exists(DATA_DIR):
        found.append(ERROR_CATALOG["HC-7002"])
    if not os.path.exists(JWT_KEY_FILE):
        found.append(ERROR_CATALOG["HC-7001"])

    return found


# ==================== API路由 ====================

@router.get("/report")
async def diagnostics_report():
    found = _run_diagnostics()
    return {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "system": {
            "platform": __import__("platform").system(),
            "hostname": __import__("platform").node(),
            "python": __import__("platform").python_version(),
        },
        "totalErrorCodes": len(ERROR_CATALOG),
        "detectedIssues": len(found),
        "issues": found,
        "categories": CATEGORY_MAP,
        "status": "HEALTHY" if len(found) == 0 else ("WARNING" if any(i["severity"] == "warning" for i in found) else "CRITICAL"),
    }


@router.get("/error-catalog")
async def error_catalog():
    categorized = {}
    for code, info in ERROR_CATALOG.items():
        cat = info["category"]
        cat_name = CATEGORY_MAP.get(cat, "其他")
        if cat_name not in categorized:
            categorized[cat_name] = []
        categorized[cat_name].append(info)
    return {
        "total": len(ERROR_CATALOG),
        "categories": CATEGORY_MAP,
        "errors": categorized,
    }


@router.get("/error/{code}")
async def get_error(code: str):
    code = code.upper()
    if code not in ERROR_CATALOG:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail=f"错误码 {code} 不存在")
    return ERROR_CATALOG[code]


@router.post("/fix/{code}")
async def fix_error(code: str):
    code = code.upper()
    if code not in ERROR_CATALOG:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail=f"错误码 {code} 不存在")

    error_info = ERROR_CATALOG[code]

    # HC-7002: 创建缺失目录
    if code == "HC-7002":
        try:
            os.makedirs(DATA_DIR, exist_ok=True)
            return FixResult(code=code, success=True, message="缺失目录已创建", details=f"已创建目录: {DATA_DIR}")
        except Exception as e:
            return FixResult(code=code, success=False, message="创建目录失败", details=str(e))

    # HC-7001: 重新生成JWT密钥
    if code == "HC-7001":
        try:
            os.makedirs(DATA_DIR, exist_ok=True)
            import secrets
            new_key = secrets.token_hex(32)
            with open(JWT_KEY_FILE, "w") as f:
                f.write(new_key)
            return FixResult(code=code, success=True, message="JWT密钥已重新生成", details="新密钥已保存，下次启动生效")
        except Exception as e:
            return FixResult(code=code, success=False, message="JWT密钥重新生成失败", details=str(e))

    # HC-3001/HC-3004: 清理锁文件和临时文件
    if code in ("HC-3001", "HC-3004"):
        cleaned = 0
        try:
            for pattern in ["*.lock", "*.tmp", "*.bak"]:
                for f in glob.glob(os.path.join(DATA_DIR, pattern)):
                    os.remove(f)
                    cleaned += 1
            return FixResult(code=code, success=True, message=f"已清理{cleaned}个临时/锁文件", details="磁盘空间已部分释放")
        except Exception as e:
            return FixResult(code=code, success=False, message="清理文件失败", details=str(e))

    # 其他错误码暂不支持自动修复
    return FixResult(
        code=code, success=False,
        message=f"错误码 {code} 暂不支持自动修复",
        details=f"建议手动处理: {error_info['solution']}"
    )


@router.post("/fix-all")
async def fix_all():
    found = _run_diagnostics()
    results = []
    fixed_count = 0
    for issue in found:
        code = issue["code"]
        result = await fix_error(code)
        results.append(result)
        if result.success:
            fixed_count += 1
    return {
        "totalIssues": len(found),
        "fixedCount": fixed_count,
        "results": results,
        "message": f"已修复 {fixed_count}/{len(found)} 个问题",
    }
