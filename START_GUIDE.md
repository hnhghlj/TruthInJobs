# 🚀 WelfareWatch 启动指南

## 当前准备工作

在开始之前，请确保以下准备工作已完成：

### ✅ 必需软件
- [ ] Python 3.8+ （推荐 3.11）
- [ ] MySQL 8.0+ （或 5.7+）
- [ ] Node.js 18+ （用于前端）
- [ ] Git

### ✅ 可选软件
- [ ] Redis（用于缓存，可选）
- [ ] Docker（用于容器化部署）

---

## 🎯 方式一：快速开始（推荐新手）

### 步骤 1：准备 MySQL 数据库

```bash
# 启动 MySQL（如果未启动）
# Windows:
net start MySQL80

# 创建数据库（一条命令搞定）
mysql -u root -p < backend\setup_mysql.sql
# 输入 MySQL root 密码
```

### 步骤 2：安装后端依赖

```bash
# 进入后端目录
cd backend

# 创建虚拟环境（推荐）
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# Linux/Mac:
# source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 步骤 3：配置环境变量

```bash
# 复制环境变量模板
copy .env.example .env

# 编辑 .env 文件，修改以下内容：
# SECRET_KEY=你的密钥（可以先不改，仅用于开发）
# DB_PASSWORD=你的MySQL密码（重要！）
# JWT_SECRET_KEY=JWT密钥（可以先不改）
```

**最小配置示例：**
```ini
# .env 文件
DEBUG=True
SECRET_KEY=django-insecure-dev-key-only
DB_PASSWORD=你的MySQL密码
JWT_SECRET_KEY=jwt-dev-key-only
ALLOWED_HOSTS=localhost,127.0.0.1
```

### 步骤 4：检查数据库连接

```bash
# 检查 MySQL 连接
python check_mysql.py

# 如果看到 ✅ 所有检查通过，说明数据库配置正确
```

### 步骤 5：初始化数据库

```bash
# 创建数据表
python manage.py migrate

# 初始化示例数据（可选，推荐）
python init_data.py
```

### 步骤 6：启动后端服务器

```bash
# 启动开发服务器
python manage.py runserver

# 看到以下信息表示启动成功：
# Starting development server at http://127.0.0.1:8000/
```

**打开浏览器测试：**
- 后端 API：http://localhost:8000/api/
- API 文档：http://localhost:8000/api/docs/
- 健康检查：http://localhost:8000/health/

### 步骤 7：启动前端（新终端）

```bash
# 打开新终端，进入前端目录
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev

# 看到：
# VITE ready in xxx ms
# Local: http://localhost:5173/
```

**访问前端：**
- 前端页面：http://localhost:5173/

### 步骤 8：登录测试

使用初始化的测试账号登录：

```
管理员账号：
用户名: admin
密码: admin123

审核员账号：
用户名: moderator
密码: moderator123

普通用户：
用户名: user1
密码: password123
```

---

## 🐳 方式二：使用 Docker（推荐生产环境）

### 前提条件
- 已安装 Docker
- 已安装 Docker Compose

### 步骤 1：配置环境变量

```bash
# 复制后端环境变量
copy backend\.env.example backend\.env

# 编辑 backend\.env，修改以下内容：
# ENVIRONMENT=production
# DEBUG=False
# SECRET_KEY=生产环境密钥（必须修改！）
# DB_PASSWORD=安全的数据库密码
```

### 步骤 2：启动所有服务

```bash
# 启动所有服务（MySQL、Redis、后端、前端）
docker-compose up -d

# 查看服务状态
docker-compose ps
```

### 步骤 3：初始化数据库

```bash
# 执行数据库迁移
docker-compose exec backend python manage.py migrate

# 创建管理员账号
docker-compose exec backend python manage.py createsuperuser

# 初始化示例数据（可选）
docker-compose exec backend python init_data.py
```

### 步骤 4：访问应用

- 前端：http://localhost
- 后端 API：http://localhost:8000
- API 文档：http://localhost:8000/api/docs/

### Docker 常用命令

```bash
# 查看日志
docker-compose logs -f backend
docker-compose logs -f frontend

# 停止服务
docker-compose stop

# 重启服务
docker-compose restart

# 停止并删除容器
docker-compose down

# 进入容器
docker-compose exec backend bash
docker-compose exec frontend sh
```

---

## 🛠️ 常见问题排查

### 问题 1：MySQL 连接失败

```bash
# 检查 MySQL 是否运行
# Windows:
net start MySQL80

# 测试连接
python backend\check_mysql.py
```

**可能原因：**
1. MySQL 服务未启动
2. 数据库不存在
3. 密码错误

**解决方法：**
```bash
# 重新创建数据库
mysql -u root -p
# 输入密码后执行：
CREATE DATABASE welfarewatch CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
exit;
```

### 问题 2：端口被占用

```bash
# 检查端口占用
# Windows:
netstat -ano | findstr :8000
netstat -ano | findstr :5173

# 杀掉占用端口的进程
taskkill /PID <进程ID> /F
```

### 问题 3：依赖安装失败

```bash
# 升级 pip
python -m pip install --upgrade pip

# 清理缓存重新安装
pip cache purge
pip install -r requirements.txt --no-cache-dir
```

### 问题 4：前端无法连接后端

**检查 CORS 配置：**

```python
# backend/welfare_watch/settings.py
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]
```

### 问题 5：数据库迁移错误

```bash
# 删除迁移文件重新生成
# 注意：这会丢失数据！
python manage.py migrate --fake-initial
```

---

## 📊 验证安装

### 1. 检查后端健康状态

```bash
# 在浏览器或终端访问
curl http://localhost:8000/health/

# 应该返回：
# {"status": "healthy", "checks": {...}}
```

### 2. 检查 API 文档

访问：http://localhost:8000/api/docs/

应该能看到完整的 Swagger API 文档

### 3. 检查前端页面

访问：http://localhost:5173/

应该能看到首页

### 4. 测试登录

1. 点击"登录"
2. 使用 `admin` / `admin123`
3. 登录成功后应该能看到用户信息

---

## 🎓 下一步

### 开发环境

```bash
# 后端开发
cd backend
python manage.py runserver

# 查看日志
python view_logs.py

# 运行测试
pytest

# 代码检查
flake8 apps utils config
black apps utils config
```

### 学习资源

- 📖 [企业级开发指南](../ENTERPRISE_GUIDE.md)
- 🔒 [安全政策](../SECURITY.md)
- 📝 [快速参考](../QUICK_REFERENCE.md)
- 🚀 [部署指南](../DEPLOY.md)

---

## 📞 获取帮助

### 遇到问题？

1. 查看日志文件：`backend/logs/welfarewatch.log`
2. 查看错误日志：`backend/logs/welfarewatch_error.log`
3. 查看文档：[ENTERPRISE_GUIDE.md](../ENTERPRISE_GUIDE.md)

### 日志查看

```bash
# 查看一般日志
python backend\view_logs.py

# 查看错误日志
python backend\view_logs.py welfarewatch_error.log

# 分析日志
python backend\analyze_logs.py
```

---

## ✅ 启动检查清单

开始开发前，确认以下项目：

- [ ] MySQL 服务已启动
- [ ] 数据库已创建（welfarewatch）
- [ ] .env 文件已配置
- [ ] 依赖已安装（requirements.txt）
- [ ] 数据库迁移已完成（migrate）
- [ ] 后端服务器已启动（8000端口）
- [ ] 前端服务器已启动（5173端口）
- [ ] 能访问 API 文档（/api/docs/）
- [ ] 能访问前端页面
- [ ] 能成功登录

---

## 🎉 完成！

如果所有步骤都成功，恭喜你！你已经成功启动了 WelfareWatch 项目！

**现在你可以：**
1. 浏览公司列表
2. 查看评价详情
3. 发布新评价
4. 管理审核内容（管理员）

**祝你开发愉快！** 🚀

