# 数据库迁移说明

## 问题说明

如果你遇到 `Failed to open the referenced table 'users'` 错误，说明数据库中可能有旧数据或迁移顺序有问题。

## 解决方案

### 方式一：重置数据库（推荐，适合开发环境）

```bash
# 1. 删除数据库
mysql -u root -p
DROP DATABASE welfarewatch;
CREATE DATABASE welfarewatch CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
exit;

# 2. 删除所有迁移记录（如果有）
# 删除 apps/*/migrations/ 目录下的所有文件（除了 __init__.py）

# 3. 重新生成迁移文件
python manage.py makemigrations

# 4. 执行迁移
python manage.py migrate

# 5. 初始化数据
python init_data.py
```

### 方式二：使用提供的脚本

```bash
# Windows
reset_database.bat

# Linux/Mac
bash reset_database.sh
```

## 时区配置

项目已配置为中国时区（Asia/Shanghai），数据库连接也会自动设置为 +08:00。

所有时间字段都会自动转换为中国时间。

