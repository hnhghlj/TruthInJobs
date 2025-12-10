from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'logs', views.ModerationLogViewSet, basename='moderation-log')
router.register(r'reports', views.ReportViewSet, basename='report')
router.register(r'', views.ModerationViewSet, basename='moderation')

app_name = 'moderation'

urlpatterns = [
    path('', include(router.urls)),
]

