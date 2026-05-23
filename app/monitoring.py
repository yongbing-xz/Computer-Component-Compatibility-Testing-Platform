import os
import platform
import subprocess
import sys
import time

from fastapi import APIRouter

from app.config import settings

router = APIRouter(prefix="/api/monitoring", tags=["系统监控"])

_start_time = time.time()


# ==================== 跨平台系统信息获取（替代psutil） ====================

def _get_cpu_info() -> dict:
    """获取CPU信息"""
    info = {
        "usage": 0.0,
        "cores": os.cpu_count() or 1,
        "threads": os.cpu_count() or 1,
        "frequency": 0,
        "modelName": platform.processor() or "Unknown",
    }

    # CPU使用率
    try:
        if sys.platform == "win32":
            # Windows: 使用wmic
            result = subprocess.run(
                ["wmic", "cpu", "get", "loadpercentage"],
                capture_output=True, text=True, timeout=5,
            )
            for line in result.stdout.strip().split("\n"):
                line = line.strip()
                if line.isdigit():
                    info["usage"] = float(line)
                    break
        else:
            # Linux/macOS: 读取/proc/stat或使用top
            try:
                with open("/proc/stat", "r") as f:
                    line1 = f.readline()
                    vals1 = list(map(int, line1.split()[1:]))
                    time.sleep(0.1)
                    f.seek(0)
                    line2 = f.readline()
                    vals2 = list(map(int, line2.split()[1:]))
                    d_idle = vals2[3] - vals1[3]
                    d_total = sum(vals2) - sum(vals1)
                    if d_total > 0:
                        info["usage"] = round((1 - d_idle / d_total) * 100, 1)
            except (FileNotFoundError, PermissionError):
                pass
    except Exception:
        pass

    # CPU频率
    try:
        if sys.platform == "win32":
            result = subprocess.run(
                ["wmic", "cpu", "get", "maxclockspeed"],
                capture_output=True, text=True, timeout=5,
            )
            for line in result.stdout.strip().split("\n"):
                line = line.strip()
                if line.isdigit():
                    info["frequency"] = float(line)
                    break
        else:
            try:
                with open("/sys/devices/system/cpu/cpu0/cpufreq/cpuinfo_max_freq", "r") as f:
                    info["frequency"] = round(int(f.read().strip()) / 1000)
            except (FileNotFoundError, PermissionError):
                pass
    except Exception:
        pass

    # 物理核心数
    try:
        if sys.platform == "win32":
            result = subprocess.run(
                ["wmic", "cpu", "get", "NumberOfCores"],
                capture_output=True, text=True, timeout=5,
            )
            for line in result.stdout.strip().split("\n"):
                line = line.strip()
                if line.isdigit():
                    info["cores"] = int(line)
                    break
        else:
            try:
                with open("/proc/cpuinfo", "r") as f:
                    cores = set()
                    for line in f:
                        if line.startswith("core id"):
                            cores.add(line.strip())
                    if cores:
                        info["cores"] = len(cores)
            except (FileNotFoundError, PermissionError):
                pass
    except Exception:
        pass

    return info


def _get_memory_info() -> dict:
    """获取内存信息"""
    info = {"total": 0, "used": 0, "available": 0, "usagePercent": 0.0}

    try:
        if sys.platform == "win32":
            import ctypes
            kernel32 = ctypes.windll.kernel32
            c_ulonglong = ctypes.c_ulonglong

            class MEMORYSTATUSEX(ctypes.Structure):
                _fields_ = [
                    ("dwLength", ctypes.c_ulong),
                    ("dwMemoryLoad", ctypes.c_ulong),
                    ("ullTotalPhys", c_ulonglong),
                    ("ullAvailPhys", c_ulonglong),
                    ("ullTotalPageFile", c_ulonglong),
                    ("ullAvailPageFile", c_ulonglong),
                    ("ullTotalVirtual", c_ulonglong),
                    ("ullAvailVirtual", c_ulonglong),
                    ("ullAvailExtendedVirtual", c_ulonglong),
                ]

            stat = MEMORYSTATUSEX()
            stat.dwLength = ctypes.sizeof(stat)
            kernel32.GlobalMemoryStatusEx(ctypes.byref(stat))
            info["total"] = stat.ullTotalPhys
            info["available"] = stat.ullAvailPhys
            info["used"] = stat.ullTotalPhys - stat.ullAvailPhys
            info["usagePercent"] = stat.dwMemoryLoad
        else:
            # Linux: 读取/proc/meminfo
            try:
                mem_data = {}
                with open("/proc/meminfo", "r") as f:
                    for line in f:
                        parts = line.split()
                        if len(parts) >= 2:
                            key = parts[0].rstrip(":")
                            val = int(parts[1]) * 1024  # kB -> bytes
                            mem_data[key] = val
                info["total"] = mem_data.get("MemTotal", 0)
                info["available"] = mem_data.get("MemAvailable", 0)
                info["used"] = info["total"] - info["available"]
                if info["total"] > 0:
                    info["usagePercent"] = round(info["used"] / info["total"] * 100, 1)
            except (FileNotFoundError, PermissionError):
                pass
    except Exception:
        pass

    return info


def _get_disk_info() -> dict:
    """获取磁盘信息"""
    info = {"total": 0, "used": 0, "free": 0, "usagePercent": 0.0}

    try:
        if sys.platform == "win32":
            path = os.environ.get("SystemDrive", "C:\\")
        else:
            path = "/"
        usage = os.statvfs(path) if sys.platform != "win32" else None

        if sys.platform == "win32":
            import ctypes
            free_bytes = ctypes.c_ulonglong(0)
            total_bytes = ctypes.c_ulonglong(0)
            ctypes.windll.kernel32.GetDiskFreeSpaceExW(
                path, None, ctypes.pointer(total_bytes), ctypes.pointer(free_bytes)
            )
            info["total"] = total_bytes.value
            info["free"] = free_bytes.value
            info["used"] = total_bytes.value - free_bytes.value
        else:
            info["total"] = usage.f_blocks * usage.f_frsize
            info["free"] = usage.f_bavail * usage.f_frsize
            info["used"] = info["total"] - info["free"]

        if info["total"] > 0:
            info["usagePercent"] = round(info["used"] / info["total"] * 100, 1)
    except Exception:
        pass

    return info


def _get_network_info() -> dict:
    """获取网络信息"""
    info = {"bytesSent": 0, "bytesRecv": 0, "packetsSent": 0, "packetsRecv": 0}

    try:
        if sys.platform == "win32":
            # Windows: 使用 typeperf 获取网络字节
            result = subprocess.run(
                ["typeperf", "\\Network Interface(*)\\Bytes Received/sec", "-sc", "1"],
                capture_output=True, text=True, timeout=5,
            )
            total_recv = 0
            total_sent = 0
            for line in result.stdout.split("\n"):
                if line.startswith('"\\\\'):
                    parts = line.split('","')
                    if len(parts) >= 3:
                        try:
                            val = float(parts[2].strip('"').replace('"', ''))
                            total_recv += val
                        except (ValueError, IndexError):
                            pass
            result2 = subprocess.run(
                ["typeperf", "\\Network Interface(*)\\Bytes Sent/sec", "-sc", "1"],
                capture_output=True, text=True, timeout=5,
            )
            for line in result2.stdout.split("\n"):
                if line.startswith('"\\\\'):
                    parts = line.split('","')
                    if len(parts) >= 3:
                        try:
                            val = float(parts[2].strip('"').replace('"', ''))
                            total_sent += val
                        except (ValueError, IndexError):
                            pass
            # typeperf返回的是速率(bytes/sec)，累计值用netstat
            result3 = subprocess.run(
                ["netstat", "-s", "-p", "ip"],
                capture_output=True, text=True, timeout=5,
            )
            for line in result3.stdout.split("\n"):
                line_lower = line.strip().lower()
                # 兼容中英文
                if any(kw in line_lower for kw in ["received headers", "received header", "收到的头"]):
                    parts = line.strip().split("=")
                    if len(parts) == 2:
                        try:
                            info["bytesRecv"] = int(parts[1].strip().replace(",", ""))
                        except ValueError:
                            pass
                elif any(kw in line_lower for kw in ["sent headers", "sent header", "发送的头"]):
                    parts = line.strip().split("=")
                    if len(parts) == 2:
                        try:
                            info["bytesSent"] = int(parts[1].strip().replace(",", ""))
                        except ValueError:
                            pass
        else:
            try:
                with open("/proc/net/dev", "r") as f:
                    f.readline()  # skip header
                    f.readline()  # skip header
                    for line in f:
                        parts = line.split()
                        if len(parts) >= 10:
                            iface = parts[0].rstrip(":")
                            if iface == "lo":
                                continue
                            info["bytesRecv"] += int(parts[1])
                            info["packetsRecv"] += int(parts[2])
                            info["bytesSent"] += int(parts[9])
                            info["packetsSent"] += int(parts[10])
            except (FileNotFoundError, PermissionError):
                pass
    except Exception:
        pass

    return info


def _get_process_info() -> dict:
    """获取当前进程信息"""
    info = {"pid": os.getpid(), "threads": 1, "memoryMB": 0.0}

    try:
        import threading
        info["threads"] = threading.active_count()
    except Exception:
        pass

    try:
        if sys.platform == "win32":
            # Windows: 使用ctypes直接获取进程内存
            import ctypes
            from ctypes import wintypes
            kernel32 = ctypes.windll.kernel32
            psapi = ctypes.windll.psapi

            PROCESS_QUERY_INFORMATION = 0x0400
            PROCESS_VM_READ = 0x0010

            class PROCESS_MEMORY_COUNTERS(ctypes.Structure):
                _fields_ = [
                    ("cb", ctypes.c_ulong),
                    ("PageFaultCount", ctypes.c_ulong),
                    ("PeakWorkingSetSize", ctypes.c_size_t),
                    ("WorkingSetSize", ctypes.c_size_t),
                    ("QuotaPeakPagedPoolUsage", ctypes.c_size_t),
                    ("QuotaPagedPoolUsage", ctypes.c_size_t),
                    ("QuotaPeakNonPagedPoolUsage", ctypes.c_size_t),
                    ("QuotaNonPagedPoolUsage", ctypes.c_size_t),
                    ("PagefileUsage", ctypes.c_size_t),
                    ("PeakPagefileUsage", ctypes.c_size_t),
                ]

            handle = kernel32.OpenProcess(
                PROCESS_QUERY_INFORMATION | PROCESS_VM_READ,
                False, os.getpid()
            )
            if handle:
                counters = PROCESS_MEMORY_COUNTERS()
                counters.cb = ctypes.sizeof(counters)
                if psapi.GetProcessMemoryInfo(handle, ctypes.byref(counters), counters.cb):
                    info["memoryMB"] = round(counters.WorkingSetSize / 1024 / 1024, 1)
                kernel32.CloseHandle(handle)
        else:
            try:
                with open(f"/proc/{os.getpid()}/status", "r") as f:
                    for line in f:
                        if line.startswith("VmRSS:"):
                            kb = int(line.split()[1])
                            info["memoryMB"] = round(kb / 1024, 1)
                            break
            except (FileNotFoundError, PermissionError):
                pass
    except Exception:
        pass

    return info


# ==================== API路由 ====================

@router.get("/health")
async def health_check():
    return {
        "status": "UP",
        "service": "Hardware Compatibility Detection System",
        "version": "1.0.0",
        "python": platform.python_version(),
        "platform": platform.system(),
        "uptime": round(time.time() - _start_time, 1),
    }


@router.get("/dashboard")
async def dashboard():
    return {
        "cpu": _get_cpu_info(),
        "memory": _get_memory_info(),
        "disk": _get_disk_info(),
        "network": _get_network_info(),
        "system": {
            "platform": platform.system(),
            "platformRelease": platform.release(),
            "platformVersion": platform.version(),
            "architecture": platform.machine(),
            "hostname": platform.node(),
            "pythonVersion": platform.python_version(),
            "uptime": round(time.time() - _start_time, 1),
        },
        "process": _get_process_info(),
    }


@router.get("/metrics")
async def metrics():
    cpu_info = _get_cpu_info()
    mem_info = _get_memory_info()

    swap_info = {"total": 0, "used": 0, "free": 0, "percent": 0.0}
    try:
        if sys.platform == "win32":
            import ctypes
            kernel32 = ctypes.windll.kernel32
            c_ulonglong = ctypes.c_ulonglong

            class MEMORYSTATUSEX(ctypes.Structure):
                _fields_ = [
                    ("dwLength", ctypes.c_ulong),
                    ("dwMemoryLoad", ctypes.c_ulong),
                    ("ullTotalPhys", c_ulonglong),
                    ("ullAvailPhys", c_ulonglong),
                    ("ullTotalPageFile", c_ulonglong),
                    ("ullAvailPageFile", c_ulonglong),
                    ("ullTotalVirtual", c_ulonglong),
                    ("ullAvailVirtual", c_ulonglong),
                    ("ullAvailExtendedVirtual", c_ulonglong),
                ]

            stat = MEMORYSTATUSEX()
            stat.dwLength = ctypes.sizeof(stat)
            kernel32.GlobalMemoryStatusEx(ctypes.byref(stat))
            swap_total = stat.ullTotalPageFile - stat.ullTotalPhys
            swap_free = stat.ullAvailPageFile - stat.ullAvailPhys
            if swap_total > 0:
                swap_info = {
                    "total": swap_total,
                    "used": swap_total - swap_free,
                    "free": swap_free,
                    "percent": round((swap_total - swap_free) / swap_total * 100, 1) if swap_total > 0 else 0,
                }
        else:
            try:
                with open("/proc/meminfo", "r") as f:
                    mem_data = {}
                    for line in f:
                        parts = line.split()
                        if len(parts) >= 2:
                            key = parts[0].rstrip(":")
                            val = int(parts[1]) * 1024
                            mem_data[key] = val
                swap_total = mem_data.get("SwapTotal", 0)
                swap_free = mem_data.get("SwapFree", 0)
                swap_info = {
                    "total": swap_total,
                    "used": swap_total - swap_free,
                    "free": swap_free,
                    "percent": round((swap_total - swap_free) / swap_total * 100, 1) if swap_total > 0 else 0,
                }
            except (FileNotFoundError, PermissionError):
                pass
    except Exception:
        pass

    return {
        "cpu": {
            "overall": cpu_info["usage"],
            "perCore": [cpu_info["usage"]],
        },
        "memory": {
            "total": mem_info["total"],
            "available": mem_info["available"],
            "used": mem_info["used"],
            "free": mem_info["total"] - mem_info["used"],
            "percent": mem_info["usagePercent"],
        },
        "swap": swap_info,
        "loadAvg": {
            "1min": 0.0,
            "5min": 0.0,
            "15min": 0.0,
        },
    }
