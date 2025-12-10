"""
URL configuration for welfare_watch project.
企业级路由配置
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from utils.health import HealthCheckView, ReadinessCheckView, LivenessCheckView

# API版本
API_VERSION = 'v1'

urlpatterns = [
    # Django 管理后台
    path('admin/', admin.site.urls),
    
    # 健康检查端点（用于负载均衡器和监控）
    path('health/', HealthCheckView.as_view(), name='health'),
    path('ready/', ReadinessCheckView.as_view(), name='ready'),
    path('alive/', LivenessCheckView.as_view(), name='alive'),
    
    # API endpoints (versioned)
    path(f'api/{API_VERSION}/accounts/', include('apps.accounts.urls')),
    path(f'api/{API_VERSION}/companies/', include('apps.companies.urls')),
    path(f'api/{API_VERSION}/reviews/', include('apps.reviews.urls')),
    path(f'api/{API_VERSION}/moderation/', include('apps.moderation.urls')),
    
    # API endpoints (兼容旧版本，不带版本号)
    path('api/accounts/', include('apps.accounts.urls')),
    path('api/companies/', include('apps.companies.urls')),
    path('api/reviews/', include('apps.reviews.urls')),
    path('api/moderation/', include('apps.moderation.urls')),
    
    # CKEditor
    path('ckeditor/', include('ckeditor_uploader.urls')),
    
    # API documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]

# 开发环境配置
if settings.DEBUG:
    # 静态文件和媒体文件
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    
    # Django Debug Toolbar
    try:
        import debug_toolbar
        urlpatterns = [
            path('__debug__/', include(debug_toolbar.urls)),
        ] + urlpatterns
    except ImportError:
        pass

# 自定义错误处理
handler404 = 'utils.views.error_404'
handler500 = 'utils.views.error_500'

