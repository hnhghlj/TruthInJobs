# 🚀 Windows 系统完整启动指南

## ⚠️ 重要提示

**请按照以下步骤一步一步执行，不要跳过任何步骤！**

---

## 📋 准备工作

### 1. 确认软件已安装

打开 PowerShell 或 CMD，检查：

```bash
# 检查 Python（需要 3.8+）
python --version
# 应该显示：Python 3.x.x

# 检查 pip
pip --version

# 检查 MySQL（需要 8.0+）
mysql --version

# 检查 Node.js（需要 18+）
node --version
npm --version
```

如果任何命令报错，说明对应软件未安装或未添加到 PATH。

---

## 🎯 第一步：创建 MySQL 数据库

### 方式 A：使用 SQL 脚本（推荐）

```bash
# 在项目根目录执行
mysql -u root -p < backend\setup_mysql.sql

# 提示输入密码时，输入你的 MySQL root 密码
```

### 方式 B：手动创建

```bash
# 登录 MySQL
mysql -u root -p
# 输入密码

# 在 MySQL 命令行中执行：
CREATE DATABASE welfarewatch CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
exit;
```

---

## 🎯 第二步：配置后端

### 1. 进入后端目录

```bash
cd backend
```

### 2. 创建虚拟环境（强烈推荐）

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境（重要！）
venv\Scripts\activate

# 激活成功后，命令行前面会显示 (venv)
```

### 3. 升级 pip

```bash
python -m pip install --upgrade pip
```

### 4. 安装依赖

```bash
# 安装所有依赖（这一步很重要！）
pip install -r requirements.txt

# 安装过程可能需要 3-5 分钟，请耐心等待
# 你会看到很多安装信息滚动...
```

**常见问题：**

如果安装 `mysqlclient` 失败，尝试：

```bash
# 先安装 Visual C++ Build Tools
# 或者使用预编译的 wheel 文件
pip install mysqlclient --only-binary :all:
```

### 5. 创建环境变量文件

```bash
# 复制模板
copy .env.example .env
```

### 6. 编辑 .env 文件

```bash
# 用记事本打开
notepad .env
```

**修改以下内容：**

```ini
# 最小配置（仅开发环境）
DEBUG=True
SECRET_KEY=django-insecure-dev-key-only-for-testing
DB_PASSWORD=你的MySQL密码
JWT_SECRET_KEY=jwt-dev-key-only
ALLOWED_HOSTS=localhost,127.0.0.1
DB_NAME=welfarewatch
DB_USER=root
DB_HOST=localhost
DB_PORT=3306
```

**重要：** 
- `DB_PASSWORD` 必须改成你的 MySQL 密码
- 其他配置开发环境可以暂时不改

保存并关闭记事本。

---

## 🎯 第三步：检查数据库连接

```bash
# 确保虚拟环境已激活（命令行前面有 (venv)）
# 如果没有，执行：venv\Scripts\activate

# 检查数据库连接
python check_mysql.py
```

**期望输出：**
```
============================================================
MySQL 连接检查
============================================================

✅ MySQL 连接成功！
   版本: 8.0.x

✅ 数据库字符集配置正确
   字符集: utf8mb4
   排序规则: utf8mb4_unicode_ci

✅ 当前数据库: welfarewatch

⚠️  数据库中没有表
   请运行: python manage.py migrate

============================================================
✅ 所有检查通过！数据库配置正确。
============================================================
```

如果看到 ❌ 错误，说明数据库配置有问题，请检查：
1. MySQL 是否启动：`net start MySQL80`
2. 数据库是否存在
3. 密码是否正确

---

## 🎯 第四步：初始化数据库

```bash
# 确保虚拟环境已激活
# 确保在 backend 目录

# 创建数据表
python manage.py migrate

# 你会看到很多 "Applying..." 的输出
```

**期望输出：**
```
Operations to perform:
  Apply all migrations: accounts, admin, auth, companies, contenttypes, moderation, reviews, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  ...
  Applying sessions.0001_initial... OK
```

### 初始化示例数据（推荐）

```bash
python init_data.py
```

**期望输出：**
```
============================================================
🎉 数据初始化完成！
============================================================

📋 登录信息：
   管理员账号: admin / admin123
   审核员账号: moderator / moderator123
   普通用户: user1 / password123
   ...
============================================================
```

---

## 🎯 第五步：启动后端服务器

```bash
# 确保虚拟环境已激活
# 确保在 backend 目录

# 启动开发服务器
python manage.py runserver
```

**期望输出：**
```
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
December 09, 2024 - 10:00:00
Django version 4.2.8, using settings 'welfare_watch.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

**✅ 后端启动成功！**

### 测试后端

打开浏览器访问：
- http://localhost:8000/api/ - 应该能看到 API 根页面
- http://localhost:8000/api/docs/ - 应该能看到 Swagger 文档
- http://localhost:8000/health/ - 应该返回健康检查信息

---

## 🎯 第六步：启动前端（新终端）

**重要：不要关闭后端服务器，打开一个新的终端窗口！**

### 1. 打开新的 PowerShell 或 CMD

### 2. 进入前端目录

```bash
# 从项目根目录
cd frontend
```

### 3. 安装前端依赖

```bash
npm install

# 这个过程可能需要几分钟
# 你会看到进度条...
```

### 4. 启动前端开发服务器

```bash
npm run dev
```

**期望输出：**
```
VITE v4.x.x  ready in xxx ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
  ➜  press h to show help
```

**✅ 前端启动成功！**

---

## 🎯 第七步：访问应用

### 打开浏览器，访问：

1. **前端主页**：http://localhost:5173
   - 应该能看到 WelfareWatch 首页

2. **登录测试**：
   - 点击右上角"登录"
   - 使用账号：`admin` 密码：`admin123`
   - 登录成功后应该能看到用户信息

3. **后端 API 文档**：http://localhost:8000/api/docs/
   - 应该能看到完整的 Swagger API 文档

4. **健康检查**：http://localhost:8000/health/
   - 应该返回：`{"status": "healthy", ...}`

---

## ✅ 启动成功检查清单

确认以下所有项都正常：

- [ ] MySQL 服务已启动
- [ ] 数据库 `welfarewatch` 已创建
- [ ] Python 依赖已安装（Django 等）
- [ ] .env 文件已配置
- [ ] 数据库连接检查通过
- [ ] 数据库迁移完成
- [ ] 示例数据已初始化
- [ ] 后端服务器运行在 8000 端口
- [ ] 前端服务器运行在 5173 端口
- [ ] 能访问前端页面
- [ ] 能访问 API 文档
- [ ] 能成功登录

---

## 🐛 常见错误和解决方案

### 错误 1：`No module named 'django'`

**原因：** 依赖没有安装

**解决：**
```bash
cd backend
venv\Scripts\activate
pip install -r requirements.txt
```

### 错误 2：`OperationalError: (2003, "Can't connect to MySQL server")`

**原因：** MySQL 服务未启动

**解决：**
```bash
# 启动 MySQL 服务
net start MySQL80
```

### 错误 3：`Access denied for user 'root'@'localhost'`

**原因：** 数据库密码错误

**解决：**
1. 编辑 `backend\.env` 文件
2. 修改 `DB_PASSWORD=正确的密码`
3. 保存后重启后端服务器

### 错误 4：端口被占用

**错误信息：** `Error: That port is already in use`

**解决：**
```bash
# 查找占用端口的进程
netstat -ano | findstr :8000

# 杀掉进程
taskkill /PID <进程ID> /F
```

### 错误 5：虚拟环境未激活

**症状：** 安装的包找不到

**解决：**
```bash
cd backend
venv\Scripts\activate
# 确保命令行前面有 (venv) 标志
```

---

## 📊 服务端口说明

| 服务 | 端口 | 访问地址 |
|------|------|---------|
| 前端 | 5173 | http://localhost:5173 |
| 后端 | 8000 | http://localhost:8000 |
| MySQL | 3306 | localhost:3306 |
| Redis | 6379 | localhost:6379（可选）|

---

## 🔄 重启服务

### 停止服务

- **后端**：在后端终端按 `Ctrl + C`
- **前端**：在前端终端按 `Ctrl + C`

### 重新启动

```bash
# 后端
cd backend
venv\Scripts\activate
python manage.py runserver

# 前端（新终端）
cd frontend
npm run dev
```

---

## 📝 开发时每天的启动流程

第二次启动时，只需要：

```bash
# 终端 1 - 后端
cd backend
venv\Scripts\activate
python manage.py runserver

# 终端 2 - 前端
cd frontend
npm run dev
```

就这么简单！

---

## 🆘 还有问题？

### 查看日志

```bash
# 查看后端日志
python backend\view_logs.py

# 查看错误日志
python backend\view_logs.py welfarewatch_error.log

# 分析日志
python backend\analyze_logs.py
```

### 检查配置

```bash
# 检查数据库
python backend\check_mysql.py

# 检查 Django 配置
cd backend
python manage.py check
```

### 联系帮助

- 查看完整文档：[ENTERPRISE_GUIDE.md](ENTERPRISE_GUIDE.md)
- 查看快速参考：[QUICK_REFERENCE.md](QUICK_REFERENCE.md)

---

## 🎉 成功启动！

如果你完成了所有步骤，恭喜你！

**现在你可以：**
1. 浏览公司列表
2. 查看评价详情
3. 发布新评价（需要登录）
4. 管理审核内容（使用管理员账号）

**祝你开发愉快！** 🚀

---

**提示：** 将此文件添加到书签，下次启动时直接参考！

