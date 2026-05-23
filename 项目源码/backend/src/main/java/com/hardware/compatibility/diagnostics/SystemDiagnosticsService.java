package com.hardware.compatibility.diagnostics;

import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import javax.sql.DataSource;
import java.io.File;
import java.lang.management.ManagementFactory;
import java.lang.management.MemoryMXBean;
import java.lang.management.OperatingSystemMXBean;
import java.net.ServerSocket;
import java.sql.Connection;
import java.sql.SQLException;
import java.time.LocalDateTime;
import java.util.*;

/**
 * 系统诊断服务 — 实时检测系统各组件健康状态，输出结构化诊断报告
 */
@Slf4j
@Service
public class SystemDiagnosticsService {

    private final DataSource dataSource;

    @Value("${server.port:8080}")
    private int serverPort;

    public SystemDiagnosticsService(DataSource dataSource) {
        this.dataSource = dataSource;
    }

    /**
     * 执行全面系统诊断
     */
    public Map<String, Object> runFullDiagnostics() {
        Map<String, Object> report = new LinkedHashMap<>();
        report.put("timestamp", LocalDateTime.now().toString());
        report.put("hostname", getHostname());

        List<Map<String, Object>> issues = new ArrayList<>();

        // 1. 数据库检查
        issues.addAll(checkDatabase());
        // 2. 文件系统检查
        issues.addAll(checkFileSystem());
        // 3. 网络端口检查
        issues.addAll(checkNetwork());
        // 4. 安全检查
        issues.addAll(checkSecurity());
        // 5. 性能检查
        issues.addAll(checkPerformance());
        // 6. Java环境检查
        issues.addAll(checkJavaEnvironment());

        report.put("totalIssues", issues.size());
        report.put("criticalIssues", issues.stream().filter(i -> "CRITICAL".equals(i.get("severity"))).count());
        report.put("autoFixable", issues.stream().filter(i -> Boolean.TRUE.equals(i.get("autoFix"))).count());
        report.put("issues", issues);
        report.put("status", issues.isEmpty() ? "HEALTHY" :
            issues.stream().anyMatch(i -> "CRITICAL".equals(i.get("severity"))) ? "CRITICAL" : "WARNING");

        return report;
    }

    // ==================== 数据库检查 ====================
    private List<Map<String, Object>> checkDatabase() {
        List<Map<String, Object>> issues = new ArrayList<>();

        // 连接测试
        try (Connection conn = dataSource.getConnection()) {
            if (conn.isValid(5)) {
                log.debug("[DIAG] 数据库连接正常");
            } else {
                issues.add(buildIssue(ErrorCode.HC_1001, "CRITICAL", "数据库连接验证失败"));
            }
        } catch (SQLException e) {
            String msg = e.getMessage();
            if (msg != null && msg.contains("locked")) {
                issues.add(buildIssue(ErrorCode.HC_1001, "CRITICAL", "数据库文件被锁定: " + msg));
            } else {
                issues.add(buildIssue(ErrorCode.HC_1001, "CRITICAL", "数据库连接异常: " + msg));
            }
        }

        // 磁盘空间
        File dataDir = new File(System.getProperty("user.dir"), "data");
        if (dataDir.exists()) {
            long freeSpace = dataDir.getFreeSpace() / (1024 * 1024);
            if (freeSpace < 100) {
                issues.add(buildIssue(ErrorCode.HC_1003, "CRITICAL", "数据库磁盘剩余空间仅 " + freeSpace + "MB"));
            } else if (freeSpace < 500) {
                issues.add(buildIssue(ErrorCode.HC_1003, "WARNING", "数据库磁盘剩余空间 " + freeSpace + "MB，偏低"));
            }
        }

        return issues;
    }

    // ==================== 文件系统检查 ====================
    private List<Map<String, Object>> checkFileSystem() {
        List<Map<String, Object>> issues = new ArrayList<>();
        String userDir = System.getProperty("user.dir");

        // data目录
        File dataDir = new File(userDir, "data");
        if (!dataDir.exists()) {
            issues.add(buildIssue(ErrorCode.HC_4001, "CRITICAL", "数据目录不存在: " + dataDir.getAbsolutePath()));
        } else if (!dataDir.canWrite()) {
            issues.add(buildIssue(ErrorCode.HC_4001, "CRITICAL", "数据目录不可写: " + dataDir.getAbsolutePath()));
        }

        // 日志目录
        File logsDir = new File(userDir, "logs");
        if (!logsDir.exists()) {
            issues.add(buildIssue(ErrorCode.HC_4003, "WARNING", "日志目录不存在，将自动创建"));
        } else if (!logsDir.canWrite()) {
            issues.add(buildIssue(ErrorCode.HC_4003, "CRITICAL", "日志目录不可写"));
        }

        // 前端文件检查
        File frontendDir = new File(userDir).getParentFile();
        if (frontendDir != null) {
            File indexHtml = new File(frontendDir, "frontend-simple/index.html");
            if (!indexHtml.exists()) {
                issues.add(buildIssue(ErrorCode.HC_4002, "WARNING", "前端主页面缺失: " + indexHtml.getAbsolutePath()));
            }
            File vueVendor = new File(frontendDir, "frontend-simple/vendor/vue.global.prod.js");
            if (!vueVendor.exists()) {
                issues.add(buildIssue(ErrorCode.HC_4004, "INFO", "Vue离线包缺失，将回退CDN加载"));
            }
        }

        return issues;
    }

    // ==================== 网络端口检查 ====================
    private List<Map<String, Object>> checkNetwork() {
        List<Map<String, Object>> issues = new ArrayList<>();

        // 检查关键端口是否被占用
        int[] checkPorts = {serverPort, 8080, 3000};
        for (int port : checkPorts) {
            if (!isPortAvailable(port)) {
                // 如果是当前服务端口，说明我们自己占着，没问题
                if (port == serverPort) continue;
                issues.add(buildIssue(ErrorCode.HC_2001, "WARNING",
                    "端口 " + port + " 已被占用，可能影响相关服务"));
            }
        }

        return issues;
    }

    // ==================== 安全检查 ====================
    private List<Map<String, Object>> checkSecurity() {
        List<Map<String, Object>> issues = new ArrayList<>();
        String userDir = System.getProperty("user.dir");

        // JWT密钥检查
        File jwtKeyFile = new File(userDir, "data/.jwt-key");
        if (!jwtKeyFile.exists()) {
            issues.add(buildIssue(ErrorCode.HC_3001, "INFO", "JWT密钥文件不存在，将在首次请求时自动生成"));
        }

        return issues;
    }

    // ==================== 性能检查 ====================
    private List<Map<String, Object>> checkPerformance() {
        List<Map<String, Object>> issues = new ArrayList<>();

        // 内存检查
        MemoryMXBean memoryBean = ManagementFactory.getMemoryMXBean();
        long heapUsed = memoryBean.getHeapMemoryUsage().getUsed() / (1024 * 1024);
        long heapMax = memoryBean.getHeapMemoryUsage().getMax() / (1024 * 1024);
        double heapUsage = heapMax > 0 ? (double) heapUsed / heapMax * 100 : 0;

        if (heapUsage > 90) {
            issues.add(buildIssue(ErrorCode.HC_6003, "CRITICAL",
                String.format("JVM堆内存使用率 %.1f%% (%dMB/%dMB)", heapUsage, heapUsed, heapMax)));
        } else if (heapUsage > 75) {
            issues.add(buildIssue(ErrorCode.HC_6003, "WARNING",
                String.format("JVM堆内存使用率 %.1f%% (%dMB/%dMB)", heapUsage, heapUsed, heapMax)));
        }

        // 磁盘空间
        File root = new File("/");
        long freeGB = root.getFreeSpace() / (1024 * 1024 * 1024);
        if (freeGB < 1) {
            issues.add(buildIssue(ErrorCode.HC_6002, "CRITICAL", "系统磁盘剩余空间不足1GB"));
        } else if (freeGB < 5) {
            issues.add(buildIssue(ErrorCode.HC_6002, "WARNING", "系统磁盘剩余空间 " + freeGB + "GB，偏低"));
        }

        // 线程数
        int threadCount = ManagementFactory.getThreadMXBean().getThreadCount();
        if (threadCount > 200) {
            issues.add(buildIssue(ErrorCode.HC_6004, "WARNING", "活跃线程数: " + threadCount));
        }

        // CPU使用率
        try {
            com.sun.management.OperatingSystemMXBean osBean =
                (com.sun.management.OperatingSystemMXBean) ManagementFactory.getOperatingSystemMXBean();
            double cpuLoad = osBean.getProcessCpuLoad() * 100;
            if (cpuLoad > 80) {
                issues.add(buildIssue(ErrorCode.HC_6001, "WARNING",
                    String.format("进程CPU使用率 %.1f%%", cpuLoad)));
            }
        } catch (Exception ignored) {}

        return issues;
    }

    // ==================== Java环境检查 ====================
    private List<Map<String, Object>> checkJavaEnvironment() {
        List<Map<String, Object>> issues = new ArrayList<>();

        String javaVersion = System.getProperty("java.version");
        String javaVm = System.getProperty("java.vm.name");
        String javaHome = System.getProperty("java.home");

        // Java版本检查
        try {
            int majorVersion = Integer.parseInt(javaVersion.split("\\.")[0]);
            if (majorVersion < 17) {
                issues.add(buildIssue(ErrorCode.HC_5003, "CRITICAL",
                    "Java版本 " + javaVersion + " 低于最低要求 17"));
            }
        } catch (NumberFormatException e) {
            issues.add(buildIssue(ErrorCode.HC_5003, "WARNING",
                "无法解析Java版本: " + javaVersion));
        }

        return issues;
    }

    // ==================== 工具方法 ====================
    private Map<String, Object> buildIssue(ErrorCode errorCode, String severity, String detail) {
        Map<String, Object> issue = new LinkedHashMap<>(errorCode.toMap());
        issue.put("severity", severity);
        issue.put("detail", detail);
        issue.put("detectedAt", LocalDateTime.now().toString());
        return issue;
    }

    private boolean isPortAvailable(int port) {
        try (ServerSocket ss = new ServerSocket(port)) {
            ss.setReuseAddress(true);
            return true;
        } catch (Exception e) {
            return false;
        }
    }

    private String getHostname() {
        try {
            return java.net.InetAddress.getLocalHost().getHostName();
        } catch (Exception e) {
            return "unknown";
        }
    }
}
