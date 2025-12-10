from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'industries', views.IndustryViewSet, basename='industry')
router.register(r'', views.CompanyViewSet, basename='company')

app_name = 'companies'

urlpatterns = [
    path('', include(router.urls)),
]

