package com.hardware.compatibility.diagnostics;

import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.*;

/**
 * 系统诊断API — 提供实时诊断、错误码查询、自动修复功能
 */
@RestController
@RequestMapping("/api/diagnostics")
@RequiredArgsConstructor
public class DiagnosticsController {

    private final SystemDiagnosticsService diagnosticsService;
    private final SelfHealingService selfHealingService;

    /**
     * 执行全面系统诊断
     * GET /api/diagnostics/report
     */
    @GetMapping("/report")
    public ResponseEntity<Map<String, Object>> getDiagnosticReport() {
        return ResponseEntity.ok(diagnosticsService.runFullDiagnostics());
    }

    /**
     * 查询指定错误码详情
     * GET /api/diagnostics/error/{code}
     */
    @GetMapping("/error/{code}")
    public ResponseEntity<Map<String, Object>> getErrorDetail(@PathVariable String code) {
        ErrorCode ec = ErrorCode.fromCode(code);
        return ResponseEntity.ok(ec.toMap());
    }

    /**
     * 获取完整错误码手册
     * GET /api/diagnostics/error-catalog
     */
    @GetMapping("/error-catalog")
    public ResponseEntity<Map<String, Object>> getErrorCatalog() {
        Map<String, Object> catalog = new LinkedHashMap<>();
        catalog.put("title", "硬件兼容性检测平台 — 错误码手册");
        catalog.put("version", "1.0.0");
        catalog.put("totalCodes", ErrorCode.values().length);

        Map<String, List<Map<String, Object>>> categories = new LinkedHashMap<>();
        categories.put("HC-1xxx 数据库层", filterByPrefix("HC-1"));
        categories.put("HC-2xxx 网络层", filterByPrefix("HC-2"));
        categories.put("HC-3xxx 安全层", filterByPrefix("HC-3"));
        categories.put("HC-4xxx 文件系统", filterByPrefix("HC-4"));
        categories.put("HC-5xxx 应用层", filterByPrefix("HC-5"));
        categories.put("HC-6xxx 性能层", filterByPrefix("HC-6"));
        categories.put("HC-9xxx 未知/外部", filterByPrefix("HC-9"));

        catalog.put("categories", categories);
        return ResponseEntity.ok(catalog);
    }

    /**
     * 尝试自动修复指定错误
     * POST /api/diagnostics/fix/{code}
     */
    @PostMapping("/fix/{code}")
    public ResponseEntity<Map<String, Object>> fixIssue(@PathVariable String code) {
        return ResponseEntity.ok(selfHealingService.attemptFix(code));
    }

    /**
     * 一键修复所有可自动修复的问题
     * POST /api/diagnostics/fix-all
     */
    @PostMapping("/fix-all")
    public ResponseEntity<Map<String, Object>> fixAll() {
        return ResponseEntity.ok(selfHealingService.fixAll(diagnosticsService));
    }

    private List<Map<String, Object>> filterByPrefix(String prefix) {
        List<Map<String, Object>> list = new ArrayList<>();
        for (ErrorCode ec : ErrorCode.values()) {
            if (ec.getCode().startsWith(prefix)) {
                list.add(ec.toMap());
            }
        }
        return list;
    }
}
