from rest_framework import viewsets, filters, permissions
from django_filters.rest_framework import DjangoFilterBackend
from .models import Industry, Company
from .serializers import (
    IndustrySerializer,
    CompanyListSerializer,
    CompanyDetailSerializer,
    CompanyCreateSerializer
)


class IndustryViewSet(viewsets.ReadOnlyModelViewSet):
    """行业视图集（只读）"""
    queryset = Industry.objects.all()
    serializer_class = IndustrySerializer
    permission_classes = [permissions.AllowAny]


class CompanyViewSet(viewsets.ModelViewSet):
    """公司视图集"""
    queryset = Company.objects.filter(is_active=True)
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['industry', 'size', 'is_verified']
    search_fields = ['name', 'name_en', 'location', 'description']
    ordering_fields = ['review_count', 'average_rating', 'created_at']
    ordering = ['-review_count']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return CompanyListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return CompanyCreateSerializer
        return CompanyDetailSerializer
    
    def perform_create(self, serializer):
        """创建公司时，可以添加额外逻辑"""
        serializer.save()

