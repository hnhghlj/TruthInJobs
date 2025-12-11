# WelfareWatch - 公司福利评价系统

> 🏢 **企业级公司评价平台** - 帮助职场人了解公司真实待遇，做出更明智的职业选择

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/django-4.2-green.svg)](https://www.djangoproject.com/)
[![Vue](https://img.shields.io/badge/vue-3.0-brightgreen.svg)](https://vuejs.org/)

一个类似 Glassdoor/Blind 的企业级公司评价平台，采用前后端分离架构，遵循现代软件工程最佳实践。

## 📚 文档导航

- 🚀 [快速开始](#快速开始) - 5分钟快速部署
- 📖 [企业级开发指南](ENTERPRISE_GUIDE.md) - 完整的开发规范和最佳实践
- 🔒 [安全政策](SECURITY.md) - 安全规范和漏洞报告
- 📝 [变更日志](CHANGELOG_ENTERPRISE.md) - 企业级升级详情
- 🗄️ [MySQL 配置指南](backend/MYSQL_SETUP.md) - 数据库详细配置
- 📊 [日志系统指南](backend/LOGGING_GUIDE.md) - 企业级日志配置

## ✨ 特性

### 🎯 核心特性
- ✅ **匿名评价系统** - 保护用户隐私，真实反馈
- ✅ **多维度评分** - 福利待遇、工作环境、发展机会、管理水平
- ✅ **富文本支持** - 详细的评价内容，支持图片和表情
- ✅ **智能审核** - 管理员/审核员双重审核机制
- ✅ **举报系统** - 社区自治，维护内容质量

### 🔒 企业级特性
- ✅ **环境变量管理** - 安全的配置管理
- ✅ **统一响应格式** - 标准化的 API 响应
- ✅ **全局异常处理** - 优雅的错误处理
- ✅ **请求限流** - 防止恶意请求和 DDoS
- ✅ **健康检查** - 完善的监控端点
- ✅ **企业级日志** - 结构化日志和日志轮转
- ✅ **缓存系统** - Redis 缓存支持
- ✅ **Docker 支持** - 容器化部署
- ✅ **CI/CD** - 自动化测试和部署

## 🛠 技术栈

### 后端
- **框架**: Django 4.2 + Django REST Framework
- **数据库**: MySQL 8.0
- **缓存**: Redis 7.0
- **认证**: JWT
- **富文本**: CKEditor
- **API文档**: drf-spectacular (Swagger)
- **日志系统**: Python logging (企业级配置)
- **测试**: Pytest + Coverage
- **代码质量**: Flake8 + Black + MyPy

### 前端
- **框架**: Vue 3 + Vite
- **UI组件**: Element Plus
- **状态管理**: Pinia
- **路由**: Vue Router
- **HTTP客户端**: Axios
- **富文本编辑器**: WangEditor

## 核心功能

### 用户功能
- ✅ 用户注册/登录（JWT认证）
- ✅ 匿名评价公司（支持富文本）
- ✅ 多维度评分（福利待遇、工作环境、发展机会、管理水平）
- ✅ 追加评论（支持图片上传和表情）
- ✅ 浏览公司信息和评价
- ✅ 标记评价/评论为"有用"

### 审核功能
- ✅ 管理员/审核员审核评价
- ✅ 管理员/审核员审核评论
- ✅ 举报内容处理
- ✅ 审核日志记录
- ✅ 审核统计面板

### 公司管理
- ✅ 公司信息管理
- ✅ 行业分类
- ✅ 公司搜索和筛选
- ✅ 自动统计评分和评价数

## 项目结构

```
.
├── backend/                    # Django 后端
│   ├── apps/
│   │   ├── accounts/          # 用户认证
│   │   ├── companies/         # 公司管理
│   │   ├── reviews/           # 评价和评论
│   │   └── moderation/        # 审核系统
│   ├── welfare_watch/         # 项目配置
│   ├── manage.py
│   └── requirements.txt
│
├── frontend/                   # Vue 3 前端
│   ├── src/
│   │   ├── api/               # API 接口
│   │   ├── assets/            # 静态资源
│   │   ├── layouts/           # 布局组件
│   │   ├── router/            # 路由配置
│   │   ├── stores/            # Pinia 状态管理
│   │   ├── views/             # 页面组件
│   │   │   ├── auth/          # 认证页面
│   │   │   ├── admin/         # 管理后台
│   │   │   └── ...            # 其他页面
│   │   ├── App.vue
│   │   └── main.js
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
│
├── LICENSE
└── README.md
```

## 🚀 快速开始

#### 后端设置

1. **安装并配置 MySQL 数据库**

```bash
# 快速创建数据库
mysql -u root -p < backend/setup_mysql.sql
```

详细配置请参考：[MySQL 配置指南](backend/MYSQL_SETUP.md)

2. **创建虚拟环境并安装依赖**

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. **配置环境变量**

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑 .env 文件，修改必要的配置
# 至少需要修改：
# - SECRET_KEY
# - DB_PASSWORD
# - JWT_SECRET_KEY
```

4. **初始化数据库**

```bash
python manage.py makemigrations
python manage.py migrate
```

5. **创建超级管理员**

```bash
python manage.py createsuperuser
```

6. **（可选）初始化示例数据**

```bash
python init_data.py
```

7. **运行开发服务器**

```bash
python manage.py runserver
# 或使用 Makefile
make run
```

后端服务将运行在 `http://localhost:8000`

### 前端设置

1. 安装依赖：
```bash
cd frontend
npm install
```

2. 运行开发服务器：
```bash
npm run dev
```

前端服务将运行在 `http://localhost:5173`

## 📡 API 文档

启动后端服务后，访问：
- **Swagger UI**: `http://localhost:8000/api/docs/`
- **API Schema**: `http://localhost:8000/api/schema/`
- **健康检查**: `http://localhost:8000/health/`

### API 版本化

支持两种访问方式：
- 版本化：`/api/v1/accounts/`（推荐）
- 兼容旧版：`/api/accounts/`

## 🔌 主要 API 端点

### 用户认证
- `POST /api/accounts/register/` - 用户注册
- `POST /api/accounts/login/` - 用户登录
- `GET /api/accounts/me/` - 获取当前用户信息
- `PUT /api/accounts/profile/` - 更新用户信息
- `POST /api/accounts/change-password/` - 修改密码

### 公司管理
- `GET /api/companies/` - 获取公司列表
- `GET /api/companies/{id}/` - 获取公司详情
- `POST /api/companies/` - 创建公司（需要登录）
- `GET /api/companies/industries/` - 获取行业列表

### 评价管理
- `GET /api/reviews/reviews/` - 获取评价列表
- `GET /api/reviews/reviews/{id}/` - 获取评价详情
- `POST /api/reviews/reviews/` - 创建评价（需要登录）
- `POST /api/reviews/reviews/{id}/mark_helpful/` - 标记为有用
- `GET /api/reviews/reviews/my_reviews/` - 获取我的评价

### 评论管理
- `GET /api/reviews/comments/` - 获取评论列表
- `POST /api/reviews/comments/` - 创建评论（需要登录）
- `POST /api/reviews/comments/{id}/mark_helpful/` - 标记为有用

### 审核管理（需要审核员权限）
- `GET /api/moderation/pending_reviews/` - 获取待审核评价
- `GET /api/moderation/pending_comments/` - 获取待审核评论
- `POST /api/moderation/moderate_review/` - 审核评价
- `POST /api/moderation/moderate_comment/` - 审核评论
- `GET /api/moderation/statistics/` - 获取审核统计

### 举报管理
- `GET /api/moderation/reports/` - 获取举报列表
- `POST /api/moderation/reports/` - 创建举报
- `POST /api/moderation/reports/{id}/handle/` - 处理举报

## 数据模型

### 用户 (User)
- 扩展 Django 默认用户模型
- 包含用户类型（普通用户/审核员/管理员）
- 匿名昵称用于匿名发布

### 公司 (Company)
- 基本信息（名称、Logo、网站等）
- 行业分类
- 公司规模
- 统计信息（评价数、平均评分）

### 评价 (Review)
- 富文本内容
- 多维度评分
- 职位信息
- 审核状态
- 支持图片上传

### 评论 (Comment)
- 支持回复评论
- 审核状态
- 支持图片上传

### 审核日志 (ModerationLog)
- 记录所有审核操作
- 支持多种内容类型

### 举报 (Report)
- 举报类型和说明
- 处理状态和备注

## 审核流程

1. 用户发布评价/评论后，状态为"待审核"
2. 普通用户只能看到"已通过"的内容
3. 审核员可以查看所有待审核内容
4. 审核员审核后，状态变为"已通过"或"已拒绝"
5. 只有"已通过"的内容会公开显示
6. 所有审核操作都会记录日志

## 权限说明

### 普通用户
- 浏览公司和已审核的评价/评论
- 发布评价和评论（需审核）
- 标记有用
- 举报不当内容

### 审核员
- 普通用户的所有权限
- 审核评价和评论
- 查看审核统计

### 管理员
- 审核员的所有权限
- 管理用户和公司
- 查看所有审核日志

## 🔧 开发工具

### Makefile 命令（后端）

```bash
make help          # 显示所有可用命令
make install       # 安装依赖
make migrate       # 执行数据库迁移
make test          # 运行测试
make test-cov      # 运行测试并生成覆盖率报告
make lint          # 代码检查
make format        # 代码格式化
make clean         # 清理临时文件
make run           # 运行开发服务器
make logs          # 查看日志
make backup-db     # 备份数据库
```

### 健康检查端点

- `/health/` - 完整健康检查（数据库、缓存等）
- `/alive/` - 存活检查
- `/ready/` - 就绪检查

## 🚀 生产部署

详细部署指南请参考：[DEPLOY.md](DEPLOY.md)

### 生产环境检查清单

- [ ] `DEBUG=False`
- [ ] 配置强密码的 `SECRET_KEY` 和 `JWT_SECRET_KEY`
- [ ] 使用 MySQL 8.0+
- [ ] 配置 Redis 缓存
- [ ] 启用 HTTPS
- [ ] 配置 `ALLOWED_HOSTS`
- [ ] 配置 `CSRF_TRUSTED_ORIGINS`
- [ ] 使用 Gunicorn + Nginx
- [ ] 配置日志监控
- [ ] 定期数据库备份
- [ ] 配置 Sentry 错误追踪（可选）

## 🧪 测试

```bash
# 运行所有测试
cd backend
pytest

# 运行特定测试
pytest tests/test_accounts.py

# 生成覆盖率报告
pytest --cov --cov-report=html

# 查看覆盖率报告
open htmlcov/index.html
```

## 📊 代码质量

```bash
# 代码检查
flake8 apps utils config

# 代码格式化
black apps utils config

# 类型检查
mypy apps utils config
```

## 🔒 安全

- 所有敏感配置使用环境变量
- JWT Token 认证
- 请求限流（防DDoS）
- SQL 注入防护（ORM）
- XSS 防护
- CSRF 防护
- 输入验证
- 安全头配置

详细安全政策请参考：[SECURITY.md](SECURITY.md)

## 📈 性能优化

- Redis 缓存
- 数据库连接池
- 数据库索引优化
- 响应缓存装饰器
- 静态文件压缩
- CDN 支持（可选）

## 🐛 故障排除

### 常见问题

**1. 数据库连接失败**
- 检查 MySQL 是否运行
- 检查数据库配置是否正确
- 运行 `python check_mysql.py` 检查连接

**2. 前端无法连接后端**
- 检查 CORS 配置
- 检查后端是否运行
- 检查前端 API 地址配置

**3. 静态文件404**
- 运行 `python manage.py collectstatic`
- 检查 Nginx 配置

更多问题请查看：[企业级开发指南](ENTERPRISE_GUIDE.md)

## 📚 学习资源

- [Django 官方文档](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Vue 3 文档](https://vuejs.org/)
- [Element Plus](https://element-plus.org/)

## 🤝 贡献

欢迎贡献代码！请遵循以下步骤：

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

请确保：
- 代码通过所有测试
- 遵循代码规范
- 更新相关文档

## 许可证

[LICENSE](LICENSE)

## 贡献

欢迎提交 Issue 和 Pull Request！

## 联系方式

如有问题或建议，请通过以下方式联系：
- 提交 Issue
- 发送邮件

