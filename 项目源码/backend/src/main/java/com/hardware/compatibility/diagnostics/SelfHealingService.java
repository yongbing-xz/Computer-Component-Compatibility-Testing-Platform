package com.hardware.compatibility.diagnostics;

import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

import java.io.File;
import java.io.IOException;
import java.nio.file.*;
import java.time.LocalDateTime;
import java.util.*;

/**
 * 自修复服务 — 检测到问题后自动尝试修复
 */
@Slf4j
@Service
public class SelfHealingService {

    /**
     * 尝试自动修复指定错误码对应的问题
     * @return 修复结果
     */
    public Map<String, Object> attemptFix(String errorCode) {
        ErrorCode ec = ErrorCode.fromCode(errorCode);
        if (!ec.canAutoFix()) {
            return buildResult(ec, false, "该错误不支持自动修复，请手动处理: " + ec.getSolution());
        }

        log.info("[SELF-HEAL] 尝试自动修复: {} - {}", ec.getCode(), ec.getMessage());

        try {
            boolean success = switch (ec) {
                case HC_1001 -> fixDatabaseLocked();
                case HC_1002 -> fixDatabaseSchema();
                case HC_2001 -> fixPortConflict();
                case HC_3001 -> fixJwtKey();
                case HC_4001 -> fixDataDirectory();
                case HC_4003 -> fixLogsDirectory();
                case HC_5001 -> fixStartupFailure();
                case HC_6003 -> fixMemoryPressure();
                default -> false;
            };

            String msg = success ? "自动修复成功" : "自动修复失败，请手动处理: " + ec.getSolution();
            log.info("[SELF-HEAL] {} - {}", ec.getCode(), msg);
            return buildResult(ec, success, msg);

        } catch (Exception e) {
            log.error("[SELF-HEAL] 修复过程异常: {} - {}", ec.getCode(), e.getMessage());
            return buildResult(ec, false, "修复过程异常: " + e.getMessage());
        }
    }

    /**
     * 一键修复所有可自动修复的问题
     */
    public Map<String, Object> fixAll(SystemDiagnosticsService diagnostics) {
        Map<String, Object> diagReport = diagnostics.runFullDiagnostics();
        @SuppressWarnings("unchecked")
        List<Map<String, Object>> issues = (List<Map<String, Object>>) diagReport.get("issues");

        List<Map<String, Object>> fixResults = new ArrayList<>();
        int fixed = 0, failed = 0, skipped = 0;

        for (Map<String, Object> issue : issues) {
            String code = (String) issue.get("code");
            boolean autoFix = Boolean.TRUE.equals(issue.get("autoFix"));

            if (autoFix) {
                Map<String, Object> result = attemptFix(code);
                fixResults.add(result);
                if (Boolean.TRUE.equals(result.get("success"))) fixed++;
                else failed++;
            } else {
                skipped++;
                fixResults.add(Map.of(
                    "code", code,
                    "success", false,
                    "message", "不支持自动修复，需手动处理",
                    "solution", issue.get("solution")
                ));
            }
        }

        Map<String, Object> summary = new LinkedHashMap<>();
        summary.put("timestamp", LocalDateTime.now().toString());
        summary.put("totalIssues", issues.size());
        summary.put("fixed", fixed);
        summary.put("failed", failed);
        summary.put("skipped", skipped);
        summary.put("results", fixResults);
        return summary;
    }

    // ==================== 具体修复逻辑 ====================

    private boolean fixDatabaseLocked() {
        String userDir = System.getProperty("user.dir");
        File traceFile = new File(userDir, "data/hardware_checker.trace.db");
        File lockFile = new File(userDir, "data/hardware_checker.lock.db");

        boolean cleaned = false;
        if (traceFile.exists()) {
            try {
                Files.delete(traceFile.toPath());
                log.info("[SELF-HEAL] 已删除数据库trace文件: {}", traceFile.getAbsolutePath());
                cleaned = true;
            } catch (IOException e) {
                log.warn("[SELF-HEAL] 无法删除trace文件: {}", e.getMessage());
            }
        }
        if (lockFile.exists()) {
            try {
                Files.delete(lockFile.toPath());
                log.info("[SELF-HEAL] 已删除数据库lock文件: {}", lockFile.getAbsolutePath());
                cleaned = true;
            } catch (IOException e) {
                log.warn("[SELF-HEAL] 无法删除lock文件: {}", e.getMessage());
            }
        }
        return cleaned;
    }

    private boolean fixDatabaseSchema() {
        String userDir = System.getProperty("user.dir");
        File mvDb = new File(userDir, "data/hardware_checker.mv.db");
        if (mvDb.exists()) {
            try {
                // 重命名旧数据库文件作为备份
                Path backup = Paths.get(userDir, "data", "hardware_checker.mv.db.broken." + System.currentTimeMillis());
                Files.move(mvDb.toPath(), backup);
                log.info("[SELF-HEAL] 已备份损坏的数据库到: {}", backup);
                return true;
            } catch (IOException e) {
                log.warn("[SELF-HEAL] 无法备份损坏的数据库: {}", e.getMessage());
                return false;
            }
        }
        return true; // 文件不存在，无需修复
    }

    private boolean fixPortConflict() {
        // 端口冲突无法自动修复，但可以提示
        log.info("[SELF-HEAL] 端口冲突无法自动修复，建议设置 SERVER_PORT 环境变量");
        return false;
    }

    private boolean fixJwtKey() {
        String userDir = System.getProperty("user.dir");
        File keyFile = new File(userDir, "data/.jwt-key");

        // 如果密钥文件存在但可能损坏，删除后让系统重新生成
        if (keyFile.exists()) {
            try {
                Files.delete(keyFile.toPath());
                log.info("[SELF-HEAL] 已删除旧JWT密钥文件，系统将自动生成新密钥");
                return true;
            } catch (IOException e) {
                log.warn("[SELF-HEAL] 无法删除JWT密钥文件: {}", e.getMessage());
                return false;
            }
        }
        return true; // 文件不存在，JwtUtil会自动生成
    }

    private boolean fixDataDirectory() {
        String userDir = System.getProperty("user.dir");
        File dataDir = new File(userDir, "data");

        if (!dataDir.exists()) {
            try {
                Files.createDirectories(dataDir.toPath());
                log.info("[SELF-HEAL] 已创建数据目录: {}", dataDir.getAbsolutePath());
                return true;
            } catch (IOException e) {
                log.warn("[SELF-HEAL] 无法创建数据目录: {}", e.getMessage());
                return false;
            }
        }
        return true;
    }

    private boolean fixLogsDirectory() {
        String userDir = System.getProperty("user.dir");
        File logsDir = new File(userDir, "logs");

        if (!logsDir.exists()) {
            try {
                Files.createDirectories(logsDir.toPath());
                log.info("[SELF-HEAL] 已创建日志目录: {}", logsDir.getAbsolutePath());
                return true;
            } catch (IOException e) {
                log.warn("[SELF-HEAL] 无法创建日志目录: {}", e.getMessage());
                return false;
            }
        }
        return true;
    }

    private boolean fixStartupFailure() {
        // 启动失败通常是多因素导致，尝试修复最常见的原因
        boolean anyFixed = false;
        anyFixed |= fixDatabaseLocked();
        anyFixed |= fixDataDirectory();
        anyFixed |= fixLogsDirectory();
        return anyFixed;
    }

    private boolean fixMemoryPressure() {
        log.info("[SELF-HEAL] 建议增加JVM参数 -Xmx512m 或重启服务释放内存");
        System.gc();
        log.info("[SELF-HEAL] 已执行GC建议，请观察内存变化");
        return true;
    }

    // ==================== 工具方法 ====================

    private Map<String, Object> buildResult(ErrorCode ec, boolean success, String message) {
        Map<String, Object> result = new LinkedHashMap<>();
        result.put("code", ec.getCode());
        result.put("message", ec.getMessage());
        result.put("success", success);
        result.put("detail", message);
        result.put("timestamp", LocalDateTime.now().toString());
        return result;
    }
}
