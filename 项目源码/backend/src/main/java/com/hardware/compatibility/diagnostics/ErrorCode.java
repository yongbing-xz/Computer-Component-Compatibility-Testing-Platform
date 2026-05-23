package com.hardware.compatibility.diagnostics;

/**
 * 硬件兼容性检测平台 — 错误码手册
 * 
 * 编码规则: HC-XXXX
 *   HC-1xxx  数据库层
 *   HC-2xxx  网络层
 *   HC-3xxx  安全层
 *   HC-4xxx  文件系统
 *   HC-5xxx  应用层
 *   HC-6xxx  性能层
 *   HC-9xxx  未知/外部
 * 
 * 每个错误码包含:
 *   code      - 错误码
 *   message   - 简短描述
 *   cause     - 根因分析
 *   solution  - 修复方案
 *   autoFix   - 是否支持自动修复
 */
public enum ErrorCode {

    // ==================== HC-1xxx 数据库层 ====================
    HC_1001("HC-1001", "数据库连接失败",
        "H2数据库文件被锁定或损坏，通常因为上次进程未正常退出",
        "1. 关闭所有Java进程后重启 2. 删除 backend/data/hardware_checker.trace.db 3. 如仍失败，删除 .mv.db 文件重建",
        true),
    HC_1002("HC-1002", "数据库表结构异常",
        "Hibernate schema更新失败，实体类与数据库表不匹配",
        "1. 检查实体类字段与数据库列是否一致 2. 删除 .mv.db 文件让Hibernate自动重建",
        true),
    HC_1003("HC-1003", "数据库磁盘空间不足",
        "H2数据库所在磁盘空间低于100MB",
        "1. 清理磁盘空间 2. 删除过期的日志文件 3. 检查 backend/data/ 目录大小",
        false),
    HC_1004("HC-1004", "数据库读写超时",
        "数据库操作耗时超过30秒，可能因为数据量过大或磁盘IO慢",
        "1. 检查磁盘健康状态 2. 减少单次查询数据量 3. 添加索引",
        false),

    // ==================== HC-2xxx 网络层 ====================
    HC_2001("HC-2001", "端口8080被占用",
        "另一个进程正在使用8080端口，导致后端无法启动",
        "1. 关闭占用端口的进程: netstat -ano | findstr 8080 2. 或设置环境变量 SERVER_PORT=8081",
        true),
    HC_2002("HC-2002", "前端无法连接后端API",
        "前端页面打开但无法调用后端接口，通常因为后端未启动或CORS配置错误",
        "1. 确认后端已启动: 访问 http://localhost:8080/actuator/health 2. 检查WebConfig中的CORS配置",
        false),
    HC_2003("HC-2003", "JWT令牌验证失败",
        "JWT密钥文件丢失或损坏，导致已登录用户的令牌无法验证",
        "1. 删除 backend/data/.jwt-key 文件 2. 重启后端自动生成新密钥 3. 用户需重新登录",
        true),
    HC_2004("HC-2004", "API请求超时",
        "后端接口响应时间超过10秒",
        "1. 检查后端日志定位慢接口 2. 检查数据库查询是否需要优化 3. 检查系统资源使用率",
        false),

    // ==================== HC-3xxx 安全层 ====================
    HC_3001("HC-3001", "JWT密钥使用默认值",
        "JWT密钥仍为硬编码的默认值，存在严重安全风险",
        "系统会自动生成随机密钥并保存到 backend/data/.jwt-key，请勿手动修改",
        true),
    HC_3002("HC-3002", "未认证访问受保护资源",
        "用户未登录即尝试访问需要认证的API",
        "1. 先调用 /api/auth/login 获取令牌 2. 在请求头添加 Authorization: Bearer <token>",
        false),
    HC_3003("HC-3003", "CORS跨域请求被拒绝",
        "前端页面协议/域名/端口与后端不一致",
        "1. 检查 WebConfig 中的 allowedOrigins 配置 2. 确保前端通过正确地址访问",
        false),

    // ==================== HC-4xxx 文件系统 ====================
    HC_4001("HC-4001", "数据目录不存在",
        "backend/data/ 目录缺失，数据库和JWT密钥无法持久化",
        "系统会自动创建该目录，如创建失败请手动创建并检查权限",
        true),
    HC_4002("HC-4002", "前端静态文件缺失",
        "frontend-simple/index.html 或 products-data.js 文件不存在",
        "1. 确认项目完整性 2. 从Git仓库重新拉取 3. 检查 .gitignore 是否误排除了必要文件",
        false),
    HC_4003("HC-4003", "日志目录写入失败",
        "无法写入日志文件，可能因为目录权限不足",
        "1. 检查 backend/logs/ 目录权限 2. 在Linux下执行 chmod 755 backend/logs/",
        true),
    HC_4004("HC-4004", "Vue离线包缺失",
        "frontend-simple/vendor/vue.global.prod.js 不存在，前端将回退到CDN加载",
        "1. 联网时访问前端页面会自动从CDN加载 2. 手动下载: 访问 https://unpkg.com/vue@3/dist/vue.global.prod.js 保存到 vendor/ 目录",
        false),

    // ==================== HC-5xxx 应用层 ====================
    HC_5001("HC-5001", "Spring Boot启动失败",
        "后端服务无法启动，常见原因: 端口占用、数据库锁定、配置错误",
        "1. 查看 backend/logs/ 下的日志文件 2. 检查端口占用 3. 删除数据库锁文件后重试",
        true),
    HC_5002("HC-5002", "Maven依赖下载失败",
        "首次运行时Maven无法下载依赖，通常因为网络问题",
        "1. 检查网络连接 2. 配置Maven镜像源(阿里云) 3. 删除 backend/target/ 后重试",
        false),
    HC_5003("HC-5003", "Java版本不兼容",
        "当前Java版本低于17，Spring Boot 3.x 要求最低Java 17",
        "1. 安装JDK 17或更高版本 2. 使用 ONE_CLICK_START.bat 自动安装",
        false),
    HC_5004("HC-5004", "内存不足",
        "JVM堆内存不足，可能导致OOM",
        "1. 增加JVM参数: -Xmx512m 2. 关闭其他占用内存的程序 3. 检查系统可用内存",
        false),

    // ==================== HC-6xxx 性能层 ====================
    HC_6001("HC-6001", "CPU使用率过高",
        "后端进程CPU占用持续超过80%",
        "1. 检查是否有死循环或无限递归 2. 减少并发请求 3. 优化算法复杂度",
        false),
    HC_6002("HC-6002", "磁盘空间不足",
        "系统磁盘可用空间低于500MB",
        "1. 清理临时文件和日志 2. 删除不需要的文件 3. 扩展磁盘容量",
        false),
    HC_6003("HC-6003", "内存使用率过高",
        "JVM堆内存使用率持续超过85%",
        "1. 增加JVM最大堆内存 2. 检查内存泄漏 3. 重启后端服务释放内存",
        true),
    HC_6004("HC-6004", "线程数过多",
        "活跃线程数超过200，可能导致线程耗尽",
        "1. 检查是否有线程泄漏 2. 优化线程池配置 3. 重启服务",
        false),

    // ==================== HC-9xxx 未知/外部 ====================
    HC_9001("HC-9001", "未知运行时异常",
        "未预期的运行时错误，需要查看详细堆栈信息",
        "1. 查看 backend/logs/ 下的日志 2. 根据堆栈信息定位问题 3. 提交Issue",
        false),
    HC_9002("HC-9002", "配置文件解析错误",
        "application.yml 格式错误或配置项缺失",
        "1. 检查YAML缩进是否正确(使用空格而非Tab) 2. 对比默认配置文件 3. 使用YAML验证工具",
        false),
    HC_9003("HC-9003", "操作系统不兼容",
        "当前操作系统或架构不支持自动安装功能",
        "1. 手动安装JDK 17+和Maven 2. 使用标准启动脚本 3. 查看项目README获取手动安装指南",
        false);

    private final String code;
    private final String message;
    private final String cause;
    private final String solution;
    private final boolean autoFix;

    ErrorCode(String code, String message, String cause, String solution, boolean autoFix) {
        this.code = code;
        this.message = message;
        this.cause = cause;
        this.solution = solution;
        this.autoFix = autoFix;
    }

    public String getCode() { return code; }
    public String getMessage() { return message; }
    public String getCause() { return cause; }
    public String getSolution() { return solution; }
    public boolean canAutoFix() { return autoFix; }

    /**
     * 根据错误码查找
     */
    public static ErrorCode fromCode(String code) {
        for (ErrorCode ec : values()) {
            if (ec.code.equals(code)) return ec;
        }
        return HC_9001;
    }

    /**
     * 转为Map（用于API返回）
     */
    public java.util.Map<String, Object> toMap() {
        java.util.Map<String, Object> map = new java.util.LinkedHashMap<>();
        map.put("code", code);
        map.put("message", message);
        map.put("cause", cause);
        map.put("solution", solution);
        map.put("autoFix", autoFix);
        return map;
    }
}
