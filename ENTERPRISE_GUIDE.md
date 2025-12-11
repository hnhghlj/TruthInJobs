# WelfareWatch 企业级开发指南

## 📋 目录

- [概述](#概述)
- [架构设计](#架构设计)
- [开发规范](#开发规范)
- [安全规范](#安全规范)
- [性能优化](#性能优化)
- [监控和日志](#监控和日志)
- [测试规范](#测试规范)
- [部署流程](#部署流程)

## 概述

WelfareWatch 是一个企业级的公司福利评价系统，采用前后端分离架构，遵循现代软件工程最佳实践。

### 技术栈

**后端：**
- Django 4.2 + Django REST Framework
- MySQL 8.0
- Redis（缓存）
- JWT 认证
- Gunicorn + Nginx

**前端：**
- Vue 3 + Vite
- Element Plus
- Pinia（状态管理）
- Axios

**DevOps：**
- GitHub Actions（CI/CD）
- Pytest（测试）
- Flake8 + Black（代码质量）

## 架构设计

### 后端架构

```
backend/
├── apps/                    # 业务应用
│   ├── accounts/           # 用户认证
│   ├── companies/          # 公司管理
│   ├── reviews/            # 评价系统
│   └── moderation/         # 审核系统
├── config/                 # 配置管理
├── middleware/             # 自定义中间件
├── utils/                  # 工具模块
│   ├── responses.py       # 统一响应格式
│   ├── exceptions.py      # 异常处理
│   ├── decorators.py      # 装饰器
│   └── health.py          # 健康检查
└── welfare_watch/         # 项目配置
```

### 设计原则

1. **单一职责原则**：每个模块只负责一个功能
2. **开闭原则**：对扩展开放，对修改关闭
3. **依赖倒置**：依赖抽象而非具体实现
4. **接口隔离**：使用小而专的接口
5. **DRY原则**：不重复代码

## 开发规范

### 代码风格

**Python（后端）：**
- 遵循 PEP 8 规范
- 使用 Black 进行代码格式化
- 使用 Flake8 进行代码检查
- 使用类型提示（Type Hints）

```python
# 好的示例
def get_user_by_id(user_id: int) -> Optional[User]:
    """
    根据ID获取用户
    
    Args:
        user_id: 用户ID
        
    Returns:
        User对象或None
    """
    try:
        return User.objects.get(id=user_id)
    except User.DoesNotExist:
        logger.warning(f"User {user_id} not found")
        return None
```

**JavaScript（前端）：**
- 使用 ESLint
- 使用 Prettier 格式化
- 使用组合式 API（Composition API）

```javascript
// 好的示例
import { ref, computed, onMounted } from 'vue'

export default {
  setup() {
    const users = ref([])
    const loading = ref(false)
    
    const activeUsers = computed(() => {
      return users.value.filter(u => u.is_active)
    })
    
    const fetchUsers = async () => {
      loading.value = true
      try {
        users.value = await api.getUsers()
      } catch (error) {
        console.error('Failed to fetch users:', error)
      } finally {
        loading.value = false
      }
    }
    
    onMounted(() => {
      fetchUsers()
    })
    
    return { users, loading, activeUsers, fetchUsers }
  }
}
```

### 命名规范

**Python：**
- 类名：PascalCase（`UserProfile`）
- 函数/方法：snake_case（`get_user_profile`）
- 常量：UPPER_SNAKE_CASE（`MAX_LOGIN_ATTEMPTS`）
- 私有方法：_snake_case（`_validate_password`）

**JavaScript：**
- 组件名：PascalCase（`UserProfile.vue`）
- 函数/变量：camelCase（`getUserProfile`）
- 常量：UPPER_SNAKE_CASE（`API_BASE_URL`）

### 文档规范

**所有公共函数/类必须有文档字符串：**

```python
def create_review(user: User, company: Company, content: str) -> Review:
    """
    创建公司评价
    
    Args:
        user: 评价用户
        company: 被评价公司
        content: 评价内容
        
    Returns:
        Review: 创建的评价对象
        
    Raises:
        ValidationException: 当内容不符合要求时
        PermissionDeniedException: 当用户无权限时
        
    Example:
        >>> review = create_review(user, company, "很好的公司")
        >>> print(review.status)
        'pending'
    """
    # 实现代码...
```

## 安全规范

### 1. 环境变量管理

**永远不要在代码中硬编码敏感信息！**

```python
# ❌ 错误
SECRET_KEY = 'django-insecure-123456'
DB_PASSWORD = 'password123'

# ✅ 正确
from config import Config
SECRET_KEY = Config.SECRET_KEY
DB_PASSWORD = Config.DB_PASSWORD
```

### 2. 密码安全

- 使用 Django 内置的密码哈希
- 密码最小长度：8位
- 必须包含字母和数字
- 定期提醒用户修改密码

### 3. API 安全

- 使用 JWT 认证
- 实施请求限流
- 验证所有输入
- 使用 HTTPS（生产环境）
- 添加 CSRF 保护

```python
# 使用装饰器保护端点
@require_moderator
@validate_request_data(['review_id', 'action'])
def moderate_review(request):
    # 实现代码...
```

### 4. SQL 注入防护

**始终使用 ORM，避免原始 SQL：**

```python
# ❌ 危险
User.objects.raw(f"SELECT * FROM users WHERE username = '{username}'")

# ✅ 安全
User.objects.filter(username=username)
```

### 5. XSS 防护

- 前端使用 `v-text` 而非 `v-html`（除非必要）
- 后端对用户输入进行转义
- 使用 Content Security Policy

## 性能优化

### 1. 数据库优化

**使用索引：**
```python
class Review(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['company', '-created_at']),
        ]
```

**使用 select_related 和 prefetch_related：**
```python
# ❌ N+1 查询问题
reviews = Review.objects.all()
for review in reviews:
    print(review.company.name)  # 每次都查询数据库

# ✅ 优化
reviews = Review.objects.select_related('company').all()
for review in reviews:
    print(review.company.name)  # 只查询一次
```

### 2. 缓存策略

```python
from django.core.cache import cache
from utils.decorators import cache_response

@cache_response(timeout=600, key_prefix='company_list')
def list_companies(request):
    # 结果会被缓存10分钟
    companies = Company.objects.all()
    return APIResponse.success(data=companies)
```

### 3. 分页

**始终对列表接口使用分页：**
```python
from rest_framework.pagination import PageNumberPagination

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100
```

### 4. 异步任务

对于耗时操作，使用 Celery：
```python
# 发送邮件等耗时操作
@celery_app.task
def send_notification_email(user_id, message):
    # 异步执行
    pass
```

## 监控和日志

### 日志级别

- **DEBUG**：调试信息（仅开发环境）
- **INFO**：一般信息（业务流程）
- **WARNING**：警告信息（可能的问题）
- **ERROR**：错误信息（需要关注）
- **CRITICAL**：严重错误（需要立即处理）

### 日志规范

```python
import logging
logger = logging.getLogger(__name__)

# 记录业务流程
logger.info(f"User {user.id} created review for company {company.id}")

# 记录警告
logger.warning(f"User {user.id} attempted to access restricted resource")

# 记录错误
try:
    process_payment(order)
except PaymentException as e:
    logger.error(f"Payment failed for order {order.id}: {e}", exc_info=True)
```

### 性能监控

```python
from utils.decorators import log_execution_time

@log_execution_time
def complex_calculation():
    # 自动记录执行时间
    pass
```

## 测试规范

### 测试金字塔

1. **单元测试（70%）**：测试单个函数/方法
2. **集成测试（20%）**：测试模块间交互
3. **端到端测试（10%）**：测试完整流程

### 编写测试

```python
import pytest
from apps.accounts.models import User

@pytest.mark.django_db
class TestUserModel:
    """用户模型测试"""
    
    def test_create_user(self):
        """测试创建用户"""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        assert user.username == 'testuser'
        assert user.email == 'test@example.com'
        assert user.check_password('testpass123')
    
    def test_user_str_representation(self):
        """测试用户字符串表示"""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com'
        )
        
        assert str(user) == 'testuser'
```

### 运行测试

```bash
# 运行所有测试
make test

# 运行特定测试
pytest tests/test_accounts.py

# 生成覆盖率报告
make test-cov
```

### 测试覆盖率要求

- 核心业务逻辑：> 90%
- 工具函数：> 80%
- 整体覆盖率：> 70%

## 部署流程

### 开发环境

```bash
# 1. 安装依赖
make install

# 2. 配置环境变量
cp backend/.env.example backend/.env
# 编辑 .env 文件

# 3. 数据库迁移
make migrate

# 4. 初始化数据
make init-data

# 5. 运行开发服务器
make run
```

### 生产环境

```bash
# 1. 使用 Docker Compose
docker-compose up -d

# 2. 检查服务状态
docker-compose ps

# 3. 查看日志
docker-compose logs -f backend

# 4. 执行数据库迁移
docker-compose exec backend python manage.py migrate

# 5. 收集静态文件
docker-compose exec backend python manage.py collectstatic --noinput
```

### 健康检查

系统提供三个健康检查端点：

- `/health/` - 完整健康检查（数据库、缓存等）
- `/alive/` - 存活检查（进程是否运行）
- `/ready/` - 就绪检查（是否可以接收流量）

### 监控指标

- **响应时间**：API 平均响应时间 < 200ms
- **错误率**：< 0.1%
- **可用性**：> 99.9%
- **数据库连接池**：监控连接数
- **内存使用**：< 80%

## 最佳实践清单

### 开发前

- [ ] 阅读需求文档
- [ ] 设计数据模型
- [ ] 编写 API 文档
- [ ] 评审设计方案

### 开发中

- [ ] 遵循代码规范
- [ ] 编写单元测试
- [ ] 添加日志记录
- [ ] 处理异常情况
- [ ] 编写文档字符串

### 开发后

- [ ] 运行所有测试
- [ ] 代码格式化（Black/Prettier）
- [ ] 代码检查（Flake8/ESLint）
- [ ] 更新文档
- [ ] 提交代码审查

### 部署前

- [ ] 运行完整测试套件
- [ ] 检查环境变量配置
- [ ] 备份数据库
- [ ] 准备回滚方案
- [ ] 通知相关人员

### 部署后

- [ ] 检查服务状态
- [ ] 验证核心功能
- [ ] 监控错误日志
- [ ] 检查性能指标
- [ ] 更新部署文档

## 常见问题

### Q: 如何添加新的 API 端点？

1. 在对应 app 的 `views.py` 中添加视图
2. 在 `serializers.py` 中添加序列化器
3. 在 `urls.py` 中注册路由
4. 编写测试用例
5. 更新 API 文档

### Q: 如何处理敏感数据？

- 使用环境变量存储
- 不要提交到版本控制
- 使用加密存储
- 定期轮换密钥

### Q: 如何优化慢查询？

1. 使用 Django Debug Toolbar 分析
2. 添加数据库索引
3. 使用 select_related/prefetch_related
4. 添加缓存
5. 考虑异步处理

### Q: 如何处理大文件上传？

1. 使用分块上传
2. 限制文件大小
3. 使用云存储（OSS）
4. 添加进度显示
5. 异步处理

## 参考资源

- [Django 官方文档](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Vue 3 文档](https://vuejs.org/)
- [Element Plus](https://element-plus.org/)
- [Docker 文档](https://docs.docker.com/)

## 联系方式

- 技术支持：tech@welfarewatch.com
- Bug 报告：GitHub Issues
- 功能建议：GitHub Discussions

---

**最后更新：** 2024-12-09
**版本：** 1.0.0

