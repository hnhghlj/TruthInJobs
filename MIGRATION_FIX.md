# 🔧 数据库迁移问题修复指南

## 问题描述

如果你遇到以下错误：

```
django.db.utils.OperationalError: (1824, "Failed to open the referenced table 'users'")
```

或者：

```
WARNINGS:
?: (urls.W005) URL namespace 'xxx' isn't unique.
```

## ✅ 已修复的问题

### 1. URL 命名空间重复 ✅

**问题：** API 版本化导致命名空间重复

**修复：** 已更新 `backend/welfare_watch/urls.py`，v1 版本使用独立命名空间

### 2. 时区配置 ✅

**问题：** 数据库时间不是中国时间

**修复：** 已配置：
- Django TIME_ZONE = 'Asia/Shanghai'
- MySQL 连接时区 = '+08:00'

现在所有时间都会自动使用中国时区（东八区）。

## 🚀 解决数据库迁移问题

### 方式一：使用重置脚本（推荐）

```bash
# Windows
cd backend
reset_database.bat

# 按提示操作：
# 1. 输入 yes 确认
# 2. 输入 MySQL 密码
# 3. 等待完成
# 4. 选择是否初始化示例数据
```

### 方式二：手动重置（完全控制）

#### 步骤 1：删除数据库

```bash
# 登录 MySQL
mysql -u root -p

# 在 MySQL 中执行：
DROP DATABASE IF EXISTS welfarewatch;
CREATE DATABASE welfarewatch CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
exit;
```

#### 步骤 2：清理迁移文件

```bash
cd backend

# 删除所有迁移文件（保留 __init__.py）
# Windows PowerShell:
Get-ChildItem -Path apps\*\migrations\*.py -Exclude __init__.py | Remove-Item

# 或者手动删除：
# apps/accounts/migrations/ 下的所有 .py 文件（除了 __init__.py）
# apps/companies/migrations/ 下的所有 .py 文件（除了 __init__.py）
# apps/reviews/migrations/ 下的所有 .py 文件（除了 __init__.py）
# apps/moderation/migrations/ 下的所有 .py 文件（除了 __init__.py）
```

#### 步骤 3：重新生成迁移

```bash
# 确保虚拟环境已激活
venv\Scripts\activate

# 生成迁移文件
python manage.py makemigrations

# 你应该看到：
# Migrations for 'accounts':
#   apps\accounts\migrations\0001_initial.py
# Migrations for 'companies':
#   apps\companies\migrations\0001_initial.py
# ...
```

#### 步骤 4：执行迁移

```bash
python manage.py migrate

# 你应该看到：
# Operations to perform:
#   Apply all migrations: accounts, admin, auth, companies, ...
# Running migrations:
#   Applying contenttypes.0001_initial... OK
#   Applying accounts.0001_initial... OK
#   ...
```

#### 步骤 5：初始化数据

```bash
python init_data.py

# 你应该看到：
# ============================================================
# 🎉 数据初始化完成！
# ============================================================
```

### 方式三：保留数据的修复（生产环境）

如果你需要保留现有数据：

```bash
# 1. 备份数据库
mysqldump -u root -p welfarewatch > backup_$(date +%Y%m%d).sql

# 2. 尝试修复迁移
python manage.py migrate --fake-initial

# 3. 如果还有问题，查看具体错误
python manage.py showmigrations
```

## 🧪 验证修复

### 1. 检查数据库表

```bash
mysql -u root -p welfarewatch

# 在 MySQL 中：
SHOW TABLES;

# 你应该看到：
# accounts_user
# companies_company
# companies_industry
# reviews_review
# reviews_comment
# moderation_moderationlog
# moderation_report
# ...
```

### 2. 检查时区

```bash
# 启动 Django shell
python manage.py shell

# 在 shell 中：
from django.utils import timezone
from apps.accounts.models import User

# 创建测试用户
user = User.objects.create_user(username='test_tz', email='test@test.com')

# 检查时间
print(user.date_joined)  # 应该显示中国时间
print(timezone.now())    # 应该显示中国时间

# 退出
exit()
```

### 3. 测试 API

```bash
# 启动服务器
python manage.py runserver

# 在浏览器访问：
# http://localhost:8000/health/
# 应该返回：{"status": "healthy", ...}
```

## 📊 常见问题

### Q1: makemigrations 没有检测到变化

**原因：** migrations 目录不存在或没有 __init__.py

**解决：**
```bash
# 为每个 app 创建 migrations 目录
mkdir apps\accounts\migrations
mkdir apps\companies\migrations
mkdir apps\reviews\migrations
mkdir apps\moderation\migrations

# 创建 __init__.py
echo. > apps\accounts\migrations\__init__.py
echo. > apps\companies\migrations\__init__.py
echo. > apps\reviews\migrations\__init__.py
echo. > apps\moderation\migrations\__init__.py

# 再次尝试
python manage.py makemigrations
```

### Q2: 时间还是不对

**检查：**
1. MySQL 服务器时区
```sql
SELECT @@global.time_zone, @@session.time_zone;
```

2. Django 设置
```python
# settings.py
TIME_ZONE = 'Asia/Shanghai'
USE_TZ = True
```

3. 数据库连接
```python
# settings.py
DATABASES = {
    'default': {
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES',time_zone='+08:00'",
        },
    }
}
```

### Q3: 迁移卡住不动

**原因：** 可能是表被锁定

**解决：**
```sql
-- 查看锁定的表
SHOW OPEN TABLES WHERE In_use > 0;

-- 查看进程
SHOW PROCESSLIST;

-- 杀掉阻塞的进程
KILL <process_id>;
```

## 🎯 完整的重新开始流程

如果以上方法都不行，完全重新开始：

```bash
# 1. 停止所有 Django 进程
# Ctrl + C

# 2. 删除虚拟环境
cd ..
rmdir /s /q .venv

# 3. 删除数据库
mysql -u root -p
DROP DATABASE welfarewatch;
CREATE DATABASE welfarewatch CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
exit;

# 4. 重新创建虚拟环境
cd backend
python -m venv venv
venv\Scripts\activate

# 5. 安装依赖
pip install -r requirements.txt

# 6. 清理迁移文件
# 删除 apps/*/migrations/*.py（除了 __init__.py）

# 7. 生成迁移
python manage.py makemigrations

# 8. 执行迁移
python manage.py migrate

# 9. 初始化数据
python init_data.py

# 10. 启动服务器
python manage.py runserver
```

## ✅ 成功标志

如果一切正常，你应该能：

- [ ] `python manage.py migrate` 成功执行，无错误
- [ ] `python manage.py runserver` 成功启动
- [ ] 访问 http://localhost:8000/api/docs/ 看到 API 文档
- [ ] 访问 http://localhost:8000/health/ 返回健康状态
- [ ] 使用 admin/admin123 登录成功
- [ ] 创建的数据时间显示为中国时间

## 🆘 还有问题？

查看日志：
```bash
# 查看 Django 日志
python view_logs.py

# 查看错误日志
python view_logs.py error.log

# 分析日志
python analyze_logs.py
```

---

**更新日期：** 2024-12-09  
**版本：** 2.0.0

