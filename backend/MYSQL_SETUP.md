# MySQL 数据库配置指南

## 安装 MySQL

### Windows

1. 下载 MySQL 安装包：https://dev.mysql.com/downloads/mysql/
2. 运行安装程序，选择 "Server Only" 或 "Developer Default"
3. 在配置过程中设置 root 密码（请记住这个密码）
4. 完成安装后，MySQL 服务会自动启动

### Linux (Ubuntu/Debian)

```bash
# 更新软件包列表
sudo apt update

# 安装 MySQL
sudo apt install mysql-server

# 启动 MySQL 服务
sudo systemctl start mysql

# 设置 MySQL 开机自启
sudo systemctl enable mysql

# 安全配置（设置 root 密码等）
sudo mysql_secure_installation
```

### macOS

```bash
# 使用 Homebrew 安装
brew install mysql

# 启动 MySQL 服务
brew services start mysql

# 安全配置
mysql_secure_installation
```

## 创建数据库

### 方法一：使用命令行

```bash
# 登录 MySQL
mysql -u root -p
# 输入密码

# 创建数据库
CREATE DATABASE welfarewatch CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# 创建用户（可选，建议生产环境使用）
CREATE USER 'welfarewatch_user'@'localhost' IDENTIFIED BY 'your_password';

# 授予权限
GRANT ALL PRIVILEGES ON welfarewatch.* TO 'welfarewatch_user'@'localhost';

# 刷新权限
FLUSH PRIVILEGES;

# 退出
exit;
```

### 方法二：使用 SQL 文件

将以下内容保存为 `create_db.sql`：

```sql
-- 创建数据库
CREATE DATABASE IF NOT EXISTS welfarewatch 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

-- 创建用户（可选）
CREATE USER IF NOT EXISTS 'welfarewatch_user'@'localhost' IDENTIFIED BY 'your_password';

-- 授予权限
GRANT ALL PRIVILEGES ON welfarewatch.* TO 'welfarewatch_user'@'localhost';

-- 刷新权限
FLUSH PRIVILEGES;
```

执行 SQL 文件：

```bash
mysql -u root -p < create_db.sql
```

## 配置 Django

### 1. 修改 settings.py

在 `backend/welfare_watch/settings.py` 中配置数据库：

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'welfarewatch',
        'USER': 'root',  # 或 'welfarewatch_user'
        'PASSWORD': 'your_password',  # 你的 MySQL 密码
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'charset': 'utf8mb4',
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}
```

### 2. 安装 Python MySQL 驱动

```bash
# 激活虚拟环境
cd backend
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install mysqlclient
```

**Windows 注意事项：**

如果在 Windows 上安装 `mysqlclient` 遇到问题，可以：

1. 下载预编译的 wheel 文件：
   - 访问 https://www.lfd.uci.edu/~gohlke/pythonlibs/#mysqlclient
   - 下载对应 Python 版本的 whl 文件
   - 使用 `pip install mysqlclient-xxx.whl` 安装

2. 或者使用 PyMySQL 替代：
   ```bash
   pip install PyMySQL
   ```
   
   然后在 `backend/welfare_watch/__init__.py` 添加：
   ```python
   import pymysql
   pymysql.install_as_MySQLdb()
   ```

### 3. 执行数据库迁移

```bash
# 创建迁移文件
python manage.py makemigrations

# 执行迁移
python manage.py migrate

# 创建超级管理员
python manage.py createsuperuser

# 初始化示例数据（可选）
python init_data.py
```

## 常见问题

### 1. 连接被拒绝

**错误**: `Can't connect to MySQL server on 'localhost'`

**解决方案**:
```bash
# 检查 MySQL 服务是否运行
# Windows
net start MySQL80  # 或 MySQL57

# Linux
sudo systemctl status mysql

# macOS
brew services list
```

### 2. 认证插件错误

**错误**: `Authentication plugin 'caching_sha2_password' cannot be loaded`

**解决方案**:
```sql
# 登录 MySQL
mysql -u root -p

# 修改认证方式
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'your_password';
FLUSH PRIVILEGES;
```

### 3. 字符集问题

**错误**: 中文显示乱码

**解决方案**:
```sql
# 检查字符集
SHOW VARIABLES LIKE 'character%';

# 修改数据库字符集
ALTER DATABASE welfarewatch CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 4. 权限问题

**错误**: `Access denied for user`

**解决方案**:
```sql
# 检查用户权限
SHOW GRANTS FOR 'root'@'localhost';

# 重新授权
GRANT ALL PRIVILEGES ON welfarewatch.* TO 'root'@'localhost';
FLUSH PRIVILEGES;
```

### 5. 端口被占用

**错误**: `Port 3306 is already in use`

**解决方案**:
```bash
# Windows - 查找占用端口的程序
netstat -ano | findstr :3306

# Linux/macOS
lsof -i :3306

# 修改 MySQL 端口（在 my.ini/my.cnf）
[mysqld]
port=3307
```

## 性能优化建议

### 1. 调整 MySQL 配置

编辑 `my.ini` (Windows) 或 `my.cnf` (Linux/macOS)：

```ini
[mysqld]
# 字符集
character-set-server=utf8mb4
collation-server=utf8mb4_unicode_ci

# 性能优化
max_connections=500
innodb_buffer_pool_size=1G
innodb_log_file_size=256M
query_cache_size=0
query_cache_type=0

# 慢查询日志
slow_query_log=1
slow_query_log_file=/var/log/mysql/slow.log
long_query_time=2
```

### 2. 为常用字段添加索引

Django 模型中已经为常用查询字段添加了 `db_index=True`，但你可以根据实际查询需求添加更多索引。

### 3. 使用连接池

安装 django-db-connection-pool：

```bash
pip install django-db-connection-pool
```

修改 settings.py：

```python
DATABASES = {
    'default': {
        'ENGINE': 'dj_db_conn_pool.backends.mysql',
        'NAME': 'welfarewatch',
        'USER': 'root',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '3306',
        'POOL_OPTIONS': {
            'POOL_SIZE': 10,
            'MAX_OVERFLOW': 10,
        },
        'OPTIONS': {
            'charset': 'utf8mb4',
        },
    }
}
```

## 备份和恢复

### 备份数据库

```bash
# 完整备份
mysqldump -u root -p welfarewatch > backup_$(date +%Y%m%d).sql

# 只备份结构
mysqldump -u root -p --no-data welfarewatch > structure.sql

# 只备份数据
mysqldump -u root -p --no-create-info welfarewatch > data.sql

# 备份特定表
mysqldump -u root -p welfarewatch users companies > tables.sql
```

### 恢复数据库

```bash
# 恢复完整备份
mysql -u root -p welfarewatch < backup_20240101.sql

# 创建数据库后恢复
mysql -u root -p -e "CREATE DATABASE welfarewatch CHARACTER SET utf8mb4"
mysql -u root -p welfarewatch < backup.sql
```

### 自动备份脚本 (Windows)

创建 `backup.bat`：

```batch
@echo off
set BACKUP_DIR=D:\backups\welfarewatch
set DATE=%date:~0,4%%date:~5,2%%date:~8,2%
set TIME=%time:~0,2%%time:~3,2%%time:~6,2%
set TIME=%TIME: =0%

if not exist "%BACKUP_DIR%" mkdir "%BACKUP_DIR%"

mysqldump -u root -pYOUR_PASSWORD welfarewatch > "%BACKUP_DIR%\backup_%DATE%_%TIME%.sql"

echo Backup completed: %BACKUP_DIR%\backup_%DATE%_%TIME%.sql
```

### 自动备份脚本 (Linux/macOS)

创建 `backup.sh`：

```bash
#!/bin/bash
BACKUP_DIR="/var/backups/welfarewatch"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

mysqldump -u root -pYOUR_PASSWORD welfarewatch > $BACKUP_DIR/backup_$DATE.sql

# 压缩备份
gzip $BACKUP_DIR/backup_$DATE.sql

# 删除30天前的备份
find $BACKUP_DIR -name "backup_*.sql.gz" -mtime +30 -delete

echo "Backup completed: $BACKUP_DIR/backup_$DATE.sql.gz"
```

添加到 crontab（每天凌晨2点备份）：

```bash
crontab -e
0 2 * * * /path/to/backup.sh
```

## 监控和维护

### 1. 监控数据库状态

```sql
-- 查看连接数
SHOW STATUS LIKE 'Threads_connected';

-- 查看慢查询
SHOW STATUS LIKE 'Slow_queries';

-- 查看表大小
SELECT 
    table_name AS 'Table',
    ROUND(((data_length + index_length) / 1024 / 1024), 2) AS 'Size (MB)'
FROM information_schema.TABLES
WHERE table_schema = 'welfarewatch'
ORDER BY (data_length + index_length) DESC;
```

### 2. 优化表

```sql
-- 分析表
ANALYZE TABLE table_name;

-- 优化表
OPTIMIZE TABLE table_name;

-- 修复表
REPAIR TABLE table_name;
```

### 3. 清理日志

```bash
# 清理二进制日志（占用空间大）
mysql -u root -p -e "PURGE BINARY LOGS BEFORE DATE_SUB(NOW(), INTERVAL 7 DAY);"
```

## 切换到云数据库

如果要使用云数据库服务（如阿里云 RDS、腾讯云 TencentDB），只需修改连接配置：

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'welfarewatch',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': 'your-instance.mysql.rds.aliyuncs.com',  # 云数据库地址
        'PORT': '3306',
        'OPTIONS': {
            'charset': 'utf8mb4',
            'ssl': {'ssl_ca': '/path/to/ca-cert.pem'},  # 如果需要 SSL
        },
    }
}
```

## 总结

1. ✅ 安装 MySQL
2. ✅ 创建数据库 `welfarewatch`
3. ✅ 配置 Django settings.py
4. ✅ 安装 mysqlclient
5. ✅ 执行数据库迁移
6. ✅ 启动项目

如有问题，请参考上述常见问题部分或查阅 MySQL 官方文档。

