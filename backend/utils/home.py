"""
首页视图
"""
from django.http import JsonResponse
from django.views import View


class HomeView(View):
    """
    首页视图 - 返回 API 信息
    """
    
    def get(self, request):
        """返回欢迎信息和可用端点"""
        return JsonResponse({
            'message': '🎉 欢迎使用 WelfareWatch API',
            'version': '2.0.0',
            'status': 'running',
            'documentation': {
                'swagger': request.build_absolute_uri('/api/docs/'),
                'schema': request.build_absolute_uri('/api/schema/'),
            },
            'endpoints': {
                'health': request.build_absolute_uri('/health/'),
                'accounts': request.build_absolute_uri('/api/accounts/'),
                'companies': request.build_absolute_uri('/api/companies/'),
                'reviews': request.build_absolute_uri('/api/reviews/'),
                'moderation': request.build_absolute_uri('/api/moderation/'),
                'admin': request.build_absolute_uri('/admin/'),
            },
            'quick_links': {
                'API文档': request.build_absolute_uri('/api/docs/'),
                '健康检查': request.build_absolute_uri('/health/'),
                '管理后台': request.build_absolute_uri('/admin/'),
            },
            'test_accounts': {
                'admin': {
                    'username': 'admin',
                    'password': 'admin123',
                    'role': '管理员'
                },
                'moderator': {
                    'username': 'moderator',
                    'password': 'moderator123',
                    'role': '审核员'
                },
                'user': {
                    'username': 'user1',
                    'password': 'password123',
                    'role': '普通用户'
                }
            },
            'features': [
                '✅ JWT 认证',
                '✅ 企业级日志系统',
                '✅ 请求限流',
                '✅ 健康检查',
                '✅ API 文档',
                '✅ 缓存系统',
                '✅ 时区配置（中国时区）',
            ],
        }, json_dumps_params={'ensure_ascii': False, 'indent': 2})

