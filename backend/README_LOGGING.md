# 日志系统使用说明

## 🎯 快速开始

### 查看日志

```bash
# 查看最近50行一般日志
python view_logs.py general.log

# 查看最近100行错误日志
python view_logs.py error.log -n 100

# 搜索特定关键词
python view_logs.py general.log -s "用户登录"

# 只查看ERROR级别
python view_logs.py general.log -l ERROR

# 列出所有日志文件
python view_logs.py --list
```

### 分析日志

```bash
# 分析一般日志
python analyze_logs.py

# 分析错误日志
python analyze_logs.py error.log

# 显示详细错误信息
python analyze_logs.py general.log -d
```

## 📁 日志文件

| 文件 | 说明 | 级别 |
|------|------|------|
| `logs/general.log` | 一般操作日志 | INFO+ |
| `logs/error.log` | 错误日志 | ERROR+ |
| `logs/database.log` | 数据库操作日志 | WARNING+ |
| `logs/security.log` | 安全相关日志 | INFO+ |

## 💻 在代码中使用

```python
import logging

# 获取logger
logger = logging.getLogger('apps.accounts')  # 或其他模块

# 记录日志
logger.info("用户登录成功")
logger.warning("配置项缺失")
logger.error("操作失败", exc_info=True)
```

## 📚 详细文档

完整的日志使用指南请查看: [LOGGING_GUIDE.md](LOGGING_GUIDE.md)

## ⚙️ 配置

日志配置在 `welfare_watch/settings.py` 的 `LOGGING` 部分。

### 主要特性

- ✅ 自动日志轮转（10MB）
- ✅ 保留最近10个历史文件
- ✅ 按模块分类
- ✅ 结构化日志格式
- ✅ 异常堆栈追踪
- ✅ 开发/生产环境分离

## 🔍 常用命令

### 实时监控

```bash
# Linux/Mac
tail -f logs/general.log

# Windows PowerShell
Get-Content logs\general.log -Wait -Tail 50
```

### 搜索日志

```bash
# 搜索错误
grep "ERROR" logs/general.log

# 搜索特定用户
grep "user_id=123" logs/general.log

# 统计错误数
grep -c "ERROR" logs/error.log
```

## ⚠️ 注意事项

1. **不要使用 print()** - 所有输出都应该使用 logger
2. **不要记录敏感信息** - 如密码、token等
3. **使用合适的日志级别** - DEBUG用于调试，INFO用于重要操作
4. **记录异常堆栈** - 使用 `exc_info=True`

## 🛠️ 故障排查

### 日志文件不存在

```bash
# 创建logs目录
mkdir -p logs
```

### 权限问题

```bash
# Linux/Mac
chmod 755 logs
```

---

**更多信息请查看**: [LOGGING_GUIDE.md](LOGGING_GUIDE.md)

