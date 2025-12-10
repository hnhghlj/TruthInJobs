# WelfareWatch MySQL 快速入门指南

本指南将帮助你在 5 分钟内完成 MySQL 数据库配置并启动项目。

---

## 📋 前置要求

- ✅ Python 3.8+ 已安装
- ✅ Node.js 16+ 已安装
- ✅ MySQL 5.7+ / 8.0+ 已安装

---

## 🚀 快速开始（5分钟）

### 步骤 1: 安装 MySQL（如果还没有）

**Windows:**
- 下载安装包: https://dev.mysql.com/downloads/mysql/
- 运行安装程序，记住设置的 root 密码

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install mysql-server
sudo systemctl start mysql
```

**macOS:**
```bash
brew install mysql
brew services start mysql
```

### 步骤 2: 创建数据库

**方法 A - 使用快速脚本（推荐）:**
```bash
cd backend
mysql -u root -p < setup_mysql.sql
# 输入 MySQL root 密码
```

**方法 B - 手动创建:**
```bash
mysql -u root -p
# 输入密码后执行：
CREATE DATABASE welfarewatch CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
exit;
```

### 步骤 3: 配置数据库密码

编辑 `backend/welfare_watch/settings.py` 文件，找到 DATABASES 配置：

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'welfarewatch',
        'USER': 'root',
        'PASSWORD': '你的MySQL密码',  # ← 修改这里！
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'charset': 'utf8mb4',
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}
```

### 步骤 4: 检查连接（可选但推荐）

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/macOS
source venv/bin/activate

pip install -r requirements.txt
python check_mysql.py
```

如果看到 "✅ 所有检查通过！" 说明配置正确。

### 步骤 5: 启动项目

**使用自动启动脚本（最简单）:**

Windows:
```bash
start.bat
```

Linux/macOS:
```bash
chmod +x start.sh
./start.sh
```

**或手动启动:**

后端:
```bash
cd backend
source venv/bin/activate  # Windows: venv\Scripts\activate
python manage.py migrate
python init_data.py  # 初始化示例数据
python manage.py runserver
```

前端:
```bash
cd frontend
npm install
npm run dev
```

### 步骤 6: 访问应用

🎉 恭喜！现在可以访问：

- **前端**: http://localhost:5173
- **后端 API**: http://localhost:8000/api/
- **API 文档**: http://localhost:8000/api/docs/
- **管理后台**: http://localhost:8000/admin/

### 测试账号

| 角色 | 用户名 | 密码 |
|-----|--------|------|
| 管理员 | admin | admin123 |
| 审核员 | moderator | moderator123 |
| 普通用户 | user1 | password123 |

---

## ❌ 常见问题快速解决

### 问题 1: MySQL 连接被拒绝

**错误**: `Can't connect to MySQL server`

**快速解决**:
```bash
# Windows
net start MySQL80

# Linux
sudo systemctl start mysql

# macOS
brew services start mysql
```

### 问题 2: 数据库不存在

**错误**: `Unknown database 'welfarewatch'`

**快速解决**:
```bash
cd backend
mysql -u root -p < setup_mysql.sql
```

### 问题 3: 密码错误

**错误**: `Access denied for user 'root'@'localhost'`

**快速解决**:
1. 确认密码正确
2. 修改 `settings.py` 中的 PASSWORD 字段
3. 重新运行项目

### 问题 4: mysqlclient 安装失败 (Windows)

**错误**: `error: Microsoft Visual C++ 14.0 is required`

**快速解决方案 A - 使用 PyMySQL**:
```bash
pip uninstall mysqlclient
pip install PyMySQL
```

在 `backend/welfare_watch/__init__.py` 添加：
```python
import pymysql
pymysql.install_as_MySQLdb()
```

**快速解决方案 B - 使用预编译包**:
1. 访问 https://www.lfd.uci.edu/~gohlke/pythonlibs/#mysqlclient
2. 下载对应 Python 版本的 whl 文件
3. `pip install 下载的文件.whl`

### 问题 5: 端口被占用

**错误**: `Port 3306 is already in use`

**快速解决**:

修改 MySQL 端口或在 settings.py 中使用其他端口：
```python
'PORT': '3307',  # 改为其他端口
```

---

## 📚 详细文档

遇到其他问题？查看详细文档：

- **MySQL 详细配置**: [backend/MYSQL_SETUP.md](backend/MYSQL_SETUP.md)
- **完整部署指南**: [DEPLOY.md](DEPLOY.md)
- **项目说明**: [README.md](README.md)

---

## 🎯 下一步

成功启动后，你可以：

1. ✅ 注册新账号
2. ✅ 浏览公司列表
3. ✅ 发布评价（需要审核）
4. ✅ 使用管理员账号审核内容
5. ✅ 探索更多功能

---

## 💡 专业提示

### 开发环境优化

1. **使用环境变量管理配置**:
   ```bash
   pip install python-dotenv
   ```
   
   创建 `.env` 文件:
   ```env
   DB_PASSWORD=your_password
   DEBUG=True
   ```

2. **启用 MySQL 慢查询日志**:
   ```sql
   SET GLOBAL slow_query_log = 'ON';
   SET GLOBAL long_query_time = 2;
   ```

3. **定期备份数据库**:
   ```bash
   mysqldump -u root -p welfarewatch > backup.sql
   ```

### 生产环境建议

1. ✅ 使用独立的数据库用户（非 root）
2. ✅ 修改默认端口
3. ✅ 启用 SSL 连接
4. ✅ 定期备份数据
5. ✅ 监控数据库性能

---

## 🆘 获取帮助

如果遇到问题：

1. 检查 MySQL 服务是否运行
2. 运行 `python check_mysql.py` 诊断
3. 查看错误日志
4. 查阅详细文档
5. 提交 Issue

---

**祝你使用愉快！🎉**

如果这个指南对你有帮助，请给项目点个 ⭐️ Star！

