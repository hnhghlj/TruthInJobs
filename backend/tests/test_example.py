"""
示例测试文件
演示如何编写测试
"""
import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestUserAuthentication:
    """用户认证测试"""
    
    def test_user_registration(self, api_client):
        """测试用户注册"""
        url = reverse('accounts:register')
        data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'newpass123',
            'password_confirm': 'newpass123'
        }
        
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert 'user' in response.data
    
    def test_user_login(self, api_client, user):
        """测试用户登录"""
        url = reverse('accounts:login')
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_200_OK
        assert 'token' in response.data
    
    def test_get_current_user(self, authenticated_client, user):
        """测试获取当前用户信息"""
        url = reverse('accounts:current-user')
        
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['username'] == user.username


@pytest.mark.django_db
class TestCompanyAPI:
    """公司API测试"""
    
    def test_list_companies(self, api_client):
        """测试获取公司列表"""
        url = '/api/companies/'
        
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
    
    def test_create_company_requires_auth(self, api_client):
        """测试创建公司需要认证"""
        url = '/api/companies/'
        data = {
            'name': 'Test Company',
            'industry': 1
        }
        
        response = api_client.post(url, data)
        assert response.status_code in [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN]


# 添加更多测试...

