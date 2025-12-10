# 🚀 WelfareWatch 快速参考

## 一分钟快速启动

### Docker方式（最简单）
```bash
cp backend/.env.example backend/.env
docker-compose up -d
docker-compose exec backend python manage.py migrate
```

### 本地开发
```bash
# 后端
cd backend && pip install -r requirements.txt
cp .env.example .env
python manage.py migrate && python manage.py runserver

# 前端
cd frontend && npm install && npm run dev
```

## 常用命令

### 开发命令
```bash
make help          # 查看所有命令
make run           # 运行开发服务器
make test          # 运行测试
make lint          # 代码检查
make format        # 代码格式化
make logs          # 查看日志
```

### Docker命令
```bash
docker-compose up -d              # 启动服务
docker-compose down               # 停止服务
docker-compose logs -f backend    # 查看后端日志
docker-compose exec backend bash  # 进入后端容器
docker-compose restart backend    # 重启后端
```

### Django命令
```bash
python manage.py migrate          # 数据库迁移
python manage.py createsuperuser  # 创建管理员
python manage.py shell            # 进入Shell
python manage.py collectstatic    # 收集静态文件
python init_data.py               # 初始化示例数据
```

## 重要端点

### 应用访问
- 前端：http://localhost:5173 (开发) / http://localhost (生产)
- 后端：http://localhost:8000
- API文档：http://localhost:8000/api/docs/
- 管理后台：http://localhost:8000/admin/

### 健康检查
- http://localhost:8000/health/ - 完整健康检查
- http://localhost:8000/alive/ - 存活检查
- http://localhost:8000/ready/ - 就绪检查

### API版本
- 新版：`/api/v1/accounts/`
- 兼容：`/api/accounts/`

## 环境变量（必须配置）

```bash
# .env 文件最小配置
SECRET_KEY=your-secret-key-here
DB_PASSWORD=your-mysql-password
JWT_SECRET_KEY=your-jwt-secret
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

## 测试命令

```bash
pytest                      # 运行所有测试
pytest --cov               # 生成覆盖率
pytest tests/test_*.py     # 运行特定测试
pytest -v                  # 详细输出
pytest -x                  # 遇到错误停止
```

## 代码质量

```bash
flake8 apps utils config   # 代码检查
black apps utils config    # 代码格式化
mypy apps utils config     # 类型检查
```

## 日志查看

```bash
# 查看日志文件
tail -f backend/logs/welfarewatch.log
tail -f backend/logs/welfarewatch_error.log

# 使用工具
python backend/view_logs.py
python backend/analyze_logs.py
```

## 数据库操作

```bash
# 备份
mysqldump -u root -p welfarewatch > backup.sql

# 恢复
mysql -u root -p welfarewatch < backup.sql

# 连接
mysql -u root -p welfarewatch
```

## 故障排除

### 数据库连接失败
```bash
python backend/check_mysql.py
```

### 依赖问题
```bash
pip install -r backend/requirements.txt --force-reinstall
```

### 端口占用
```bash
# Linux/Mac
lsof -i :8000
kill -9 <PID>

# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### 清理缓存
```bash
make clean
find . -type d -name __pycache__ -exec rm -rf {} +
```

## 生产部署检查

- [ ] `DEBUG=False`
- [ ] 修改所有密钥
- [ ] 配置`ALLOWED_HOSTS`
- [ ] 启用HTTPS
- [ ] 配置Redis
- [ ] 设置日志监控
- [ ] 数据库备份

## 常用装饰器

```python
from utils.decorators import *

@log_execution_time
def my_function():
    pass

@cache_response(timeout=600)
def list_view(request):
    pass

@require_moderator
def moderate_view(request):
    pass

@validate_request_data(['field1', 'field2'])
def create_view(request):
    pass
```

## API响应格式

```python
from utils.responses import APIResponse

# 成功
return APIResponse.success(data={'id': 1})

# 错误
return APIResponse.error(message='错误信息')

# 创建
return APIResponse.created(data={'id': 1})

# 未授权
return APIResponse.unauthorized()

# 验证错误
return APIResponse.validation_error(errors={'field': 'error'})
```

## 异常处理

```python
from utils.exceptions import *

# 抛出业务异常
raise BusinessException('业务错误')
raise ResourceNotFoundException('资源不存在')
raise PermissionDeniedException('无权限')
raise ValidationException('验证失败', errors={})
```

## 有用的链接

- 📖 [完整文档](ENTERPRISE_GUIDE.md)
- 🔒 [安全政策](SECURITY.md)
- 📝 [变更日志](CHANGELOG_ENTERPRISE.md)
- 🚀 [部署指南](DEPLOY.md)
- 📊 [日志指南](backend/LOGGING_GUIDE.md)

## 获取帮助

- GitHub Issues
- 技术文档
- 企业级开发指南

---

**提示**: 将此文件加入书签，随时查阅！

