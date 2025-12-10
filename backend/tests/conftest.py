"""
Pytest 配置和fixtures
"""
import pytest
from django.conf import settings
from rest_framework.test import APIClient
from apps.accounts.models import User


@pytest.fixture
def api_client():
    """API客户端fixture"""
    return APIClient()


@pytest.fixture
def user(db):
    """普通用户fixture"""
    return User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass123',
        anonymous_name='测试用户'
    )


@pytest.fixture
def admin_user(db):
    """管理员fixture"""
    return User.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='admin123',
        user_type='admin'
    )


@pytest.fixture
def moderator_user(db):
    """审核员fixture"""
    return User.objects.create_user(
        username='moderator',
        email='moderator@example.com',
        password='mod123',
        user_type='moderator'
    )


@pytest.fixture
def authenticated_client(api_client, user):
    """已认证的API客户端"""
    api_client.force_authenticate(user=user)
    return api_client


@pytest.fixture
def admin_client(api_client, admin_user):
    """管理员API客户端"""
    api_client.force_authenticate(user=admin_user)
    return api_client

