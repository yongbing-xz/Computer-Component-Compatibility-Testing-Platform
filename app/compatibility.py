from typing import Optional

from fastapi import APIRouter
from pydantic import BaseModel

from app.data.products import PRODUCTS

router = APIRouter(prefix="/api/compatibility", tags=["兼容性检测"])


class ComponentSelection(BaseModel):
    cpu: Optional[int] = None
    motherboard: Optional[int] = None
    gpu: Optional[int] = None
    memory: Optional[int] = None
    nvme: Optional[int] = None
    chassis: Optional[int] = None


class CompatibilityIssue(BaseModel):
    component1: str
    component2: str
    field: str
    value1: str
    value2: str
    severity: str
    message: str


class CompatibilityResult(BaseModel):
    compatible: bool
    score: int
    issues: list[CompatibilityIssue]
    warnings: list[str]
    summary: str


def _get_product(product_id: int) -> Optional[dict]:
    for p in PRODUCTS:
        if p["id"] == product_id:
            return p
    return None


def _check_cpu_motherboard(cpu: dict, mobo: dict, issues: list, warnings: list):
    if cpu["socket"] != mobo["socket"]:
        issues.append(CompatibilityIssue(
            component1=cpu["title"], component2=mobo["title"],
            field="CPU接口", value1=cpu["socket"], value2=mobo["socket"],
            severity="error",
            message=f"CPU接口({cpu['socket']})与主板CPU接口({mobo['socket']})不兼容"
        ))
    # 内存类型兼容性
    cpu_ddr = "DDR5" if cpu["socket"] in ("LGA1700", "AM5") else "DDR4"
    if cpu["socket"] == "LGA1700":
        cpu_ddr = "DDR4/DDR5"
    mobo_ddr = mobo["specs"].get("memoryType", "")
    if cpu_ddr != "DDR4/DDR5" and mobo_ddr and mobo_ddr not in cpu_ddr.split("/"):
        issues.append(CompatibilityIssue(
            component1=cpu["title"], component2=mobo["title"],
            field="内存类型", value1=cpu_ddr, value2=mobo_ddr,
            severity="error",
            message=f"CPU支持内存类型({cpu_ddr})与主板内存类型({mobo_ddr})不匹配"
        ))


def _check_memory_motherboard(memory: dict, mobo: dict, issues: list, warnings: list):
    mem_type = memory["specs"].get("type", "")
    mobo_mem_type = mobo["specs"].get("memoryType", "")
    if mem_type != mobo_mem_type:
        issues.append(CompatibilityIssue(
            component1=memory["title"], component2=mobo["title"],
            field="DDR类型", value1=mem_type, value2=mobo_mem_type,
            severity="error",
            message=f"内存类型({mem_type})与主板内存插槽({mobo_mem_type})不兼容"
        ))


def _check_gpu_chassis(gpu: dict, chassis: dict, issues: list, warnings: list):
    gpu_length_str = gpu["specs"].get("length", "0mm").replace("mm", "")
    max_gpu_str = chassis["specs"].get("maxGpuLength", "0mm").replace("mm", "")
    try:
        gpu_len = int(gpu_length_str)
        max_len = int(max_gpu_str)
        if gpu_len > max_len:
            issues.append(CompatibilityIssue(
                component1=gpu["title"], component2=chassis["title"],
                field="显卡长度", value1=f"{gpu_len}mm", value2=f"最大{max_len}mm",
                severity="error",
                message=f"显卡长度({gpu_len}mm)超过机箱显卡限长({max_len}mm)"
            ))
        elif gpu_len > max_len * 0.85:
            warnings.append(f"显卡长度({gpu_len}mm)接近机箱限长({max_len}mm)，安装空间较紧凑")
    except ValueError:
        pass


def _check_nvme_motherboard(nvme: dict, mobo: dict, issues: list, warnings: list):
    nvme_interface = nvme["specs"].get("interface", "")
    if "M.2" not in nvme["socket"]:
        issues.append(CompatibilityIssue(
            component1=nvme["title"], component2=mobo["title"],
            field="NVMe接口", value1=nvme["socket"], value2="M.2",
            severity="error",
            message=f"NVMe固态接口({nvme['socket']})不是M.2接口"
        ))
    # PCIe版本向下兼容，仅做提示
    if "PCIe 5.0" in nvme_interface:
        mobo_pcie = mobo["specs"].get("pcieSlots", "")
        if "PCIe 5.0" not in mobo_pcie and "PCIe 4.0" not in mobo_pcie:
            warnings.append(f"NVMe({nvme_interface})需要PCIe 5.0/4.0插槽，主板仅支持{mobo_pcie}，将以较低速度运行")


@router.post("/check", response_model=CompatibilityResult)
async def check_compatibility(selection: ComponentSelection):
    issues: list[CompatibilityIssue] = []
    warnings: list[str] = []

    cpu = _get_product(selection.cpu) if selection.cpu else None
    mobo = _get_product(selection.motherboard) if selection.motherboard else None
    gpu = _get_product(selection.gpu) if selection.gpu else None
    memory = _get_product(selection.memory) if selection.memory else None
    nvme = _get_product(selection.nvme) if selection.nvme else None
    chassis = _get_product(selection.chassis) if selection.chassis else None

    # CPU ↔ 主板
    if cpu and mobo:
        _check_cpu_motherboard(cpu, mobo, issues, warnings)

    # 内存 ↔ 主板
    if memory and mobo:
        _check_memory_motherboard(memory, mobo, issues, warnings)

    # 显卡 ↔ 机箱
    if gpu and chassis:
        _check_gpu_chassis(gpu, chassis, issues, warnings)

    # NVMe ↔ 主板
    if nvme and mobo:
        _check_nvme_motherboard(nvme, mobo, issues, warnings)

    # 功耗预警
    if cpu and gpu:
        cpu_tdp = int(cpu["specs"].get("tdp", "65W").replace("W", ""))
        gpu_tdp = int(gpu["specs"].get("tdp", "0W").replace("W", ""))
        total_tdp = cpu_tdp + gpu_tdp
        if total_tdp > 600:
            warnings.append(f"CPU+GPU总功耗约{total_tdp}W，建议使用850W以上电源")
        elif total_tdp > 400:
            warnings.append(f"CPU+GPU总功耗约{total_tdp}W，建议使用650W以上电源")

    compatible = len(issues) == 0
    error_count = len(issues)
    warning_count = len(warnings)

    if error_count == 0 and warning_count == 0:
        score = 100
    elif error_count == 0:
        score = max(60, 100 - warning_count * 5)
    else:
        score = max(0, 60 - error_count * 15 - warning_count * 3)

    if compatible and warning_count == 0:
        summary = "所有组件完全兼容，可以放心搭配！"
    elif compatible:
        summary = f"组件基本兼容，但有{warning_count}项需要注意的问题"
    else:
        summary = f"发现{error_count}个兼容性问题，需要调整组件选择"

    return CompatibilityResult(
        compatible=compatible,
        score=score,
        issues=issues,
        warnings=warnings,
        summary=summary,
    )


@router.get("/products")
async def get_products(category: Optional[str] = None):
    if category:
        cat_upper = category.upper()
        # 映射到产品数据中实际使用的类别名（中文+英文兼容）
        cat_map = {
            "CPU": "CPU",
            "MB": "主板", "MOTHERBOARD": "主板", "主板": "主板",
            "GPU": "显卡", "GRAPHICS": "显卡", "显卡": "显卡",
            "RAM": "内存", "MEMORY": "内存", "内存": "内存",
            "NVME": "NVMe", "SSD": "NVMe",
            "CASE": "机箱", "CHASSIS": "机箱", "机箱": "机箱",
        }
        mapped = cat_map.get(cat_upper, category)
        return [p for p in PRODUCTS if p["category"] == mapped]
    return PRODUCTS
