# WelfareWatch 部署指南

## 目录

- [开发环境部署](#开发环境部署)
- [生产环境部署](#生产环境部署)
- [Docker 部署](#docker-部署)
- [常见问题](#常见问题)

---

## 开发环境部署

### 系统要求

- Python 3.8+
- Node.js 16+
- MySQL 5.7+ / MySQL 8.0+

### 快速开始

#### Windows 用户

双击运行 `start.bat` 脚本，或在命令行中执行：

```bash
start.bat
```

#### Linux/Mac 用户

在终端中执行：

```bash
chmod +x start.sh
./start.sh
```

### 手动部署步骤

#### 1. 后端设置

```bash
cd backend

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 数据库迁移
python manage.py makemigrations
python manage.py migrate

# 创建超级管理员（可选）
python manage.py createsuperuser

# 初始化示例数据（可选）
python init_data.py

# 启动开发服务器
python manage.py runserver
```

#### 2. 前端设置

```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

#### 3. 访问应用

- 前端: http://localhost:5173
- 后端 API: http://localhost:8000/api/
- API 文档: http://localhost:8000/api/docs/
- Django 管理后台: http://localhost:8000/admin/

---

## 生产环境部署

### 1. 服务器准备

推荐配置：
- Ubuntu 20.04 LTS
- 2核 CPU
- 4GB RAM
- 40GB 磁盘空间

### 2. 安装系统依赖

```bash
# 更新系统
sudo apt update && sudo apt upgrade -y

# 安装 Python 和相关工具
sudo apt install -y python3 python3-pip python3-venv

# 安装 Node.js
curl -fsSL https://deb.nodesource.com/setup_16.x | sudo -E bash -
sudo apt install -y nodejs

# 安装 MySQL
sudo apt install -y mysql-server

# 安装 Nginx
sudo apt install -y nginx

# 安装 Git
sudo apt install -y git
```

### 3. 配置 MySQL

```bash
# 安全配置 MySQL
sudo mysql_secure_installation

# 登录 MySQL
sudo mysql -u root -p

# 创建数据库
CREATE DATABASE welfarewatch CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# 创建用户
CREATE USER 'welfarewatch_user'@'localhost' IDENTIFIED BY 'your_secure_password';

# 授予权限
GRANT ALL PRIVILEGES ON welfarewatch.* TO 'welfarewatch_user'@'localhost';

# 刷新权限
FLUSH PRIVILEGES;

# 退出
exit;
```

### 4. 部署后端

```bash
# 克隆代码
cd /var/www
sudo git clone https://github.com/your-repo/welfarewatch.git
cd welfarewatch/backend

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
pip install gunicorn

# 创建环境配置文件
cp .env.example .env
nano .env
```

编辑 `.env` 文件：

```env
SECRET_KEY=your-very-secure-secret-key-change-this
DEBUG=False
ALLOWED_HOSTS=your-domain.com,www.your-domain.com

# MySQL 配置
DB_NAME=welfarewatch
DB_USER=welfarewatch_user
DB_PASSWORD=your_secure_password
DB_HOST=localhost
DB_PORT=3306

CORS_ALLOWED_ORIGINS=https://your-domain.com,https://www.your-domain.com

JWT_SECRET_KEY=your-jwt-secret-key
JWT_ALGORITHM=HS256
JWT_EXPIRATION_DELTA=86400
```

然后修改 `settings.py` 读取环境变量：

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DB_NAME', 'welfarewatch'),
        'USER': os.getenv('DB_USER', 'root'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'password'),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '3306'),
        'OPTIONS': {
            'charset': 'utf8mb4',
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}
```

```bash
# 收集静态文件
python manage.py collectstatic --noinput

# 数据库迁移
python manage.py migrate

# 创建超级管理员
python manage.py createsuperuser
```

### 5. 配置 Gunicorn

创建 systemd 服务文件：

```bash
sudo nano /etc/systemd/system/welfarewatch.service
```

内容：

```ini
[Unit]
Description=WelfareWatch Django Application
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/welfarewatch/backend
Environment="PATH=/var/www/welfarewatch/backend/venv/bin"
ExecStart=/var/www/welfarewatch/backend/venv/bin/gunicorn \
          --workers 3 \
          --bind unix:/var/www/welfarewatch/backend/welfarewatch.sock \
          welfare_watch.wsgi:application

[Install]
WantedBy=multi-user.target
```

启动服务：

```bash
sudo systemctl start welfarewatch
sudo systemctl enable welfarewatch
sudo systemctl status welfarewatch
```

### 6. 部署前端

```bash
cd /var/www/welfarewatch/frontend

# 安装依赖
npm install

# 构建生产版本
npm run build
```

### 7. 配置 Nginx

创建 Nginx 配置：

```bash
sudo nano /etc/nginx/sites-available/welfarewatch
```

内容：

```nginx
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;

    # 前端静态文件
    location / {
        root /var/www/welfarewatch/frontend/dist;
        try_files $uri $uri/ /index.html;
    }

    # 后端 API
    location /api/ {
        include proxy_params;
        proxy_pass http://unix:/var/www/welfarewatch/backend/welfarewatch.sock;
    }

    # Django 管理后台
    location /admin/ {
        include proxy_params;
        proxy_pass http://unix:/var/www/welfarewatch/backend/welfarewatch.sock;
    }

    # 静态文件
    location /static/ {
        alias /var/www/welfarewatch/backend/staticfiles/;
    }

    # 媒体文件
    location /media/ {
        alias /var/www/welfarewatch/backend/media/;
    }

    # 文件上传大小限制
    client_max_body_size 10M;
}
```

启用配置：

```bash
sudo ln -s /etc/nginx/sites-available/welfarewatch /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 8. 配置 SSL (推荐)

使用 Let's Encrypt 免费证书：

```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com -d www.your-domain.com
```

### 9. 设置防火墙

```bash
sudo ufw allow 'Nginx Full'
sudo ufw allow OpenSSH
sudo ufw enable
```

---

## Docker 部署

### 1. 创建 Dockerfile (后端)

`backend/Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# 安装 Python 依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn psycopg2-binary

# 复制项目文件
COPY . .

# 收集静态文件
RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "welfare_watch.wsgi:application"]
```

### 2. 创建 Dockerfile (前端)

`frontend/Dockerfile`:

```dockerfile
FROM node:16-alpine as build

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

FROM nginx:alpine

COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

### 3. 创建 docker-compose.yml

```yaml
version: '3.8'

services:
  db:
    image: postgres:14-alpine
    environment:
      POSTGRES_DB: welfarewatch
      POSTGRES_USER: welfarewatch_user
      POSTGRES_PASSWORD: secure_password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - app-network

  backend:
    build: ./backend
    environment:
      DATABASE_URL: postgresql://welfarewatch_user:secure_password@db:5432/welfarewatch
      DEBUG: "False"
      SECRET_KEY: your-secret-key
    depends_on:
      - db
    volumes:
      - static_volume:/app/staticfiles
      - media_volume:/app/media
    networks:
      - app-network

  frontend:
    build: ./frontend
    ports:
      - "80:80"
    depends_on:
      - backend
    networks:
      - app-network

volumes:
  postgres_data:
  static_volume:
  media_volume:

networks:
  app-network:
    driver: bridge
```

### 4. 启动服务

```bash
docker-compose up -d
```

---

## 常见问题

### 1. 数据库连接错误

**问题**: `django.db.utils.OperationalError: could not connect to server`

**解决方案**:
- 检查 PostgreSQL 是否正在运行
- 验证数据库配置是否正确
- 确保数据库用户有足够的权限

### 2. 静态文件 404

**问题**: 静态文件无法加载

**解决方案**:
```bash
python manage.py collectstatic --noinput
```

### 3. CORS 错误

**问题**: 前端请求后端 API 时出现 CORS 错误

**解决方案**:
- 检查 `settings.py` 中的 `CORS_ALLOWED_ORIGINS` 配置
- 确保包含前端域名

### 4. 权限错误

**问题**: `Permission denied` 错误

**解决方案**:
```bash
sudo chown -R www-data:www-data /var/www/welfarewatch
sudo chmod -R 755 /var/www/welfarewatch
```

### 5. Gunicorn 无法启动

**问题**: Gunicorn 服务启动失败

**解决方案**:
```bash
# 查看日志
sudo journalctl -u welfarewatch -n 50

# 测试 Gunicorn
cd /var/www/welfarewatch/backend
source venv/bin/activate
gunicorn welfare_watch.wsgi:application
```

---

## 性能优化建议

### 1. 数据库优化

- 为常用查询字段添加索引
- 定期清理过期数据
- 配置数据库连接池

### 2. 缓存配置

安装 Redis 并配置缓存：

```python
# settings.py
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
    }
}
```

### 3. 静态文件 CDN

将静态文件上传到 CDN，提高加载速度。

### 4. Nginx 优化

```nginx
# 启用 gzip 压缩
gzip on;
gzip_vary on;
gzip_types text/plain text/css application/json application/javascript;

# 启用缓存
location ~* \.(jpg|jpeg|png|gif|ico|css|js)$ {
    expires 1y;
    add_header Cache-Control "public, immutable";
}
```

---

## 监控和日志

### 1. 应用日志

```bash
# Django 日志
sudo journalctl -u welfarewatch -f

# Nginx 访问日志
sudo tail -f /var/log/nginx/access.log

# Nginx 错误日志
sudo tail -f /var/log/nginx/error.log
```

### 2. 监控工具推荐

- **Sentry**: 错误追踪
- **Prometheus + Grafana**: 性能监控
- **ELK Stack**: 日志分析

---

## 备份策略

### 数据库备份

```bash
# 创建备份
mysqldump -u root -p welfarewatch > backup_$(date +%Y%m%d).sql

# 自动备份脚本
cat > /usr/local/bin/backup_db.sh << 'EOF'
#!/bin/bash
BACKUP_DIR="/var/backups/welfarewatch"
mkdir -p $BACKUP_DIR
mysqldump -u root -p'your_password' welfarewatch > $BACKUP_DIR/backup_$(date +%Y%m%d_%H%M%S).sql
# 压缩备份
gzip $BACKUP_DIR/backup_$(date +%Y%m%d_%H%M%S).sql
# 保留最近30天的备份
find $BACKUP_DIR -name "backup_*.sql.gz" -mtime +30 -delete
EOF

chmod +x /usr/local/bin/backup_db.sh

# 添加到 crontab (每天凌晨2点备份)
crontab -e
0 2 * * * /usr/local/bin/backup_db.sh
```

### 媒体文件备份

```bash
# 使用 rsync 备份
rsync -avz /var/www/welfarewatch/backend/media/ /backup/media/
```

---

## 更新部署

```bash
cd /var/www/welfarewatch

# 拉取最新代码
sudo git pull

# 更新后端
cd backend
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart welfarewatch

# 更新前端
cd ../frontend
npm install
npm run build

# 重启 Nginx
sudo systemctl restart nginx
```

---

## 技术支持

如有问题，请通过以下方式联系：

- 提交 Issue: [GitHub Issues](https://github.com/your-repo/welfarewatch/issues)
- 发送邮件: support@welfarewatch.com

---

**祝您部署成功！**

