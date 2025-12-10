# WelfareWatch 日志系统指南

## 📋 概述

本项目使用企业级的日志系统，所有日志统一管理，便于调试、监控和问题追踪。

---

## 🗂️ 日志文件结构

```
backend/logs/
├── general.log      # 一般操作日志（所有 INFO 及以上级别）
├── error.log        # 错误日志（ERROR 及以上级别）
├── database.log     # 数据库操作日志（SQL 查询等）
└── security.log     # 安全相关日志（认证、授权等）
```

### 日志轮转

- 每个日志文件最大 10MB (database.log 为 5MB)
- 自动轮转，保留最近 10 个历史文件
- 旧日志自动压缩，节省空间

---

## 📊 日志级别

| 级别 | 用途 | 示例 |
|------|------|------|
| **DEBUG** | 详细的调试信息 | 函数参数、SQL查询详情 |
| **INFO** | 一般信息记录 | 用户登录、数据创建 |
| **WARNING** | 警告信息 | 配置缺失、性能问题 |
| **ERROR** | 错误信息 | 异常、失败操作 |
| **CRITICAL** | 严重错误 | 系统崩溃、数据丢失 |

---

## 💻 在代码中使用日志

### 1. 导入日志模块

```python
import logging

# 使用应用级别的 logger
logger = logging.getLogger('apps.accounts')  # 用户模块
logger = logging.getLogger('apps.companies')  # 公司模块
logger = logging.getLogger('apps.reviews')    # 评价模块
logger = logging.getLogger('apps.moderation') # 审核模块

# 脚本使用
logger = logging.getLogger('scripts')
```

### 2. 记录不同级别的日志

```python
# DEBUG - 调试信息
logger.debug(f"函数参数: user_id={user_id}, action={action}")

# INFO - 一般信息
logger.info(f"用户 {username} 登录成功")
logger.info(f"创建公司: {company.name}")

# WARNING - 警告
logger.warning(f"用户 {user_id} 尝试访问未授权资源")
logger.warning("配置项 EMAIL_BACKEND 未设置")

# ERROR - 错误
logger.error(f"数据保存失败: {e}")
logger.error(f"API 调用失败: {response.status_code}")

# CRITICAL - 严重错误
logger.critical(f"数据库连接失败，系统无法继续运行")
```

### 3. 记录异常信息

```python
try:
    # 业务逻辑
    result = dangerous_operation()
except Exception as e:
    # exc_info=True 会自动记录完整的堆栈信息
    logger.error(f"操作失败: {e}", exc_info=True)
    raise
```

### 4. 结构化日志

```python
# 推荐：使用字典格式
logger.info("用户操作", extra={
    'user_id': user.id,
    'action': 'create_review',
    'company_id': company.id,
    'ip_address': request.META.get('REMOTE_ADDR')
})

# 或者使用格式化字符串
logger.info(
    f"Review created: user_id={user.id}, "
    f"company_id={company.id}, review_id={review.id}"
)
```

---

## 📝 各模块日志示例

### accounts (用户模块)

```python
import logging
logger = logging.getLogger('apps.accounts')

# 用户注册
logger.info(f"新用户注册: {user.username}, email={user.email}")

# 用户登录
logger.info(f"用户登录: {user.username}, IP={ip_address}")

# 登录失败
logger.warning(f"登录失败: username={username}, IP={ip_address}")

# 权限检查
logger.debug(f"权限检查: user={user.id}, permission={permission}")

# 密码修改
logger.info(f"用户 {user.username} 修改密码")
```

### reviews (评价模块)

```python
import logging
logger = logging.getLogger('apps.reviews')

# 创建评价
logger.info(f"创建评价: user={user.id}, company={company.name}, title={title}")

# 评价审核
logger.info(f"评价审核: review_id={review.id}, status={status}, moderator={moderator.username}")

# 删除评价
logger.warning(f"删除评价: review_id={review.id}, user={user.id}, reason={reason}")

# 异常处理
try:
    review.save()
except Exception as e:
    logger.error(f"评价保存失败: review_id={review.id}", exc_info=True)
```

### moderation (审核模块)

```python
import logging
logger = logging.getLogger('apps.moderation')

# 内容审核
logger.info(f"审核操作: moderator={moderator.username}, action={action}, content_id={content_id}")

# 举报处理
logger.info(f"举报处理: report_id={report.id}, handler={handler.username}, result={result}")

# 敏感操作
logger.warning(f"审核员 {moderator.username} 批量通过了 {count} 条内容")
```

---

## 🔍 查看日志

### 1. 实时查看日志

**Linux/macOS:**
```bash
# 查看最新日志
tail -f logs/general.log

# 查看错误日志
tail -f logs/error.log

# 查看最后 100 行
tail -n 100 logs/general.log
```

**Windows:**
```powershell
# 使用 PowerShell
Get-Content logs\general.log -Wait -Tail 50

# 或使用记事本/VS Code 打开
notepad logs\general.log
code logs\general.log
```

### 2. 搜索日志

```bash
# 搜索特定用户的操作
grep "user_id=123" logs/general.log

# 搜索错误信息
grep "ERROR" logs/general.log

# 搜索今天的日志
grep "2024-01-15" logs/general.log

# 统计错误数量
grep -c "ERROR" logs/error.log
```

### 3. 使用 Python 查看日志

创建 `view_logs.py`:

```python
#!/usr/bin/env python
"""日志查看工具"""
import argparse
from pathlib import Path

def view_logs(log_file, lines=50, search=None, level=None):
    """查看日志文件"""
    log_path = Path('logs') / log_file
    
    if not log_path.exists():
        print(f"日志文件不存在: {log_path}")
        return
    
    with open(log_path, 'r', encoding='utf-8') as f:
        all_lines = f.readlines()
    
    # 过滤
    filtered_lines = all_lines
    if search:
        filtered_lines = [line for line in filtered_lines if search in line]
    if level:
        filtered_lines = [line for line in filtered_lines if f"[{level}]" in line]
    
    # 显示最后 N 行
    for line in filtered_lines[-lines:]:
        print(line.rstrip())

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='查看日志文件')
    parser.add_argument('log_file', choices=['general.log', 'error.log', 'database.log', 'security.log'])
    parser.add_argument('-n', '--lines', type=int, default=50, help='显示行数')
    parser.add_argument('-s', '--search', help='搜索关键词')
    parser.add_argument('-l', '--level', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'], help='日志级别')
    
    args = parser.parse_args()
    view_logs(args.log_file, args.lines, args.search, args.level)
```

使用方式:
```bash
# 查看最近 50 行一般日志
python view_logs.py general.log

# 查看最近 100 行错误日志
python view_logs.py error.log -n 100

# 搜索特定关键词
python view_logs.py general.log -s "user_id=123"

# 只查看 ERROR 级别
python view_logs.py general.log -l ERROR
```

---

## 📈 日志分析

### 统计分析脚本

创建 `analyze_logs.py`:

```python
#!/usr/bin/env python
"""日志分析工具"""
from pathlib import Path
from collections import Counter
import re

def analyze_logs(log_file='general.log'):
    """分析日志文件"""
    log_path = Path('logs') / log_file
    
    if not log_path.exists():
        print(f"日志文件不存在: {log_path}")
        return
    
    with open(log_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # 统计日志级别
    levels = Counter()
    modules = Counter()
    
    for line in lines:
        # 提取日志级别
        level_match = re.search(r'\[(DEBUG|INFO|WARNING|ERROR|CRITICAL)\]', line)
        if level_match:
            levels[level_match.group(1)] += 1
        
        # 提取模块名
        module_match = re.search(r'\] (\w+\.\w+)', line)
        if module_match:
            modules[module_match.group(1)] += 1
    
    print("=" * 60)
    print("日志分析报告")
    print("=" * 60)
    print(f"\n总日志条数: {len(lines)}")
    
    print("\n日志级别统计:")
    for level, count in sorted(levels.items()):
        print(f"  {level:10s}: {count:6d} ({count/len(lines)*100:.1f}%)")
    
    print("\n模块日志统计 (Top 10):")
    for module, count in modules.most_common(10):
        print(f"  {module:30s}: {count:6d}")
    
    print("=" * 60)

if __name__ == '__main__':
    import sys
    log_file = sys.argv[1] if len(sys.argv) > 1 else 'general.log'
    analyze_logs(log_file)
```

---

## 🚨 监控和告警

### 1. 错误日志监控

创建监控脚本 `monitor_errors.py`:

```python
#!/usr/bin/env python
"""错误日志监控"""
from pathlib import Path
import time

def monitor_errors():
    """监控错误日志"""
    log_file = Path('logs/error.log')
    
    if not log_file.exists():
        print("错误日志文件不存在")
        return
    
    # 记录文件大小
    last_size = log_file.stat().st_size
    
    print("开始监控错误日志...")
    print("按 Ctrl+C 停止")
    
    try:
        while True:
            current_size = log_file.stat().st_size
            
            if current_size > last_size:
                # 读取新增内容
                with open(log_file, 'r', encoding='utf-8') as f:
                    f.seek(last_size)
                    new_lines = f.readlines()
                
                for line in new_lines:
                    print(f"🚨 新错误: {line.rstrip()}")
                    # 这里可以添加发送邮件/短信等告警逻辑
                
                last_size = current_size
            
            time.sleep(5)  # 每5秒检查一次
    except KeyboardInterrupt:
        print("\n监控已停止")

if __name__ == '__main__':
    monitor_errors()
```

### 2. 配置邮件告警

在 `settings.py` 中配置:

```python
# 邮件配置
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your_email@gmail.com'
EMAIL_HOST_PASSWORD = 'your_password'

# 管理员邮箱（接收错误日志）
ADMINS = [
    ('Admin Name', 'admin@example.com'),
]
```

---

## 🛠️ 日志管理

### 清理旧日志

```bash
# 删除 30 天前的日志
find logs/ -name "*.log.*" -mtime +30 -delete

# 压缩旧日志
gzip logs/general.log.1
```

### 日志备份

```bash
#!/bin/bash
# 备份日志文件
BACKUP_DIR="logs_backup/$(date +%Y%m%d)"
mkdir -p $BACKUP_DIR
cp logs/*.log $BACKUP_DIR/
tar -czf logs_backup_$(date +%Y%m%d).tar.gz $BACKUP_DIR
```

---

## 📋 最佳实践

### ✅ DO (推荐做法)

1. **使用合适的日志级别**
   ```python
   logger.info("正常操作")      # 记录重要操作
   logger.error("发生错误", exc_info=True)  # 记录异常
   ```

2. **记录足够的上下文信息**
   ```python
   logger.info(f"用户 {user.id} 创建了评价 {review.id}")
   ```

3. **使用异常堆栈**
   ```python
   try:
       risky_operation()
   except Exception as e:
       logger.error("操作失败", exc_info=True)
   ```

4. **结构化日志**
   ```python
   logger.info("订单创建", extra={
       'order_id': order.id,
       'user_id': user.id,
       'amount': order.amount
   })
   ```

### ❌ DON'T (避免的做法)

1. **不要使用 print()**
   ```python
   # ❌ 错误
   print(f"用户登录: {user.username}")
   
   # ✅ 正确
   logger.info(f"用户登录: {user.username}")
   ```

2. **不要记录敏感信息**
   ```python
   # ❌ 错误
   logger.info(f"用户密码: {password}")
   
   # ✅ 正确
   logger.info(f"用户 {user.id} 修改了密码")
   ```

3. **不要滥用 DEBUG 级别**
   ```python
   # ❌ 在生产环境记录每个查询
   logger.debug(f"SQL: {query}")
   ```

4. **不要记录过多信息**
   ```python
   # ❌ 记录巨大的对象
   logger.info(f"数据: {huge_object}")
   
   # ✅ 只记录关键信息
   logger.info(f"数据 ID: {obj.id}, 大小: {len(huge_object)}")
   ```

---

## 🔧 故障排查

### 日志文件不生成

1. 检查 logs 目录是否存在
2. 检查文件权限
3. 检查 settings.py 中的日志配置

### 日志文件过大

1. 检查日志轮转配置
2. 调整 maxBytes 和 backupCount
3. 清理旧日志文件

### 性能问题

1. 在生产环境关闭 DEBUG 日志
2. 使用异步日志处理
3. 将日志写入到专门的日志服务器

---

## 📚 参考资源

- [Python logging 官方文档](https://docs.python.org/3/library/logging.html)
- [Django logging 文档](https://docs.djangoproject.com/en/4.2/topics/logging/)
- [12-Factor App: Logs](https://12factor.net/logs)

---

**日志是系统的眼睛，合理使用日志能够极大提高开发和运维效率！** 👁️

