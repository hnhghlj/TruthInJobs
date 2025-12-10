from rest_framework import serializers
from .models import Industry, Company


class IndustrySerializer(serializers.ModelSerializer):
    """行业序列化器"""
    
    class Meta:
        model = Industry
        fields = ('id', 'name', 'description', 'created_at')


class CompanyListSerializer(serializers.ModelSerializer):
    """公司列表序列化器"""
    industry_name = serializers.CharField(source='industry.name', read_only=True)
    
    class Meta:
        model = Company
        fields = (
            'id', 'name', 'name_en', 'logo', 'industry', 'industry_name',
            'size', 'location', 'review_count', 'average_rating',
            'is_verified', 'created_at'
        )


class CompanyDetailSerializer(serializers.ModelSerializer):
    """公司详情序列化器"""
    industry_name = serializers.CharField(source='industry.name', read_only=True)
    
    class Meta:
        model = Company
        fields = (
            'id', 'name', 'name_en', 'logo', 'industry', 'industry_name',
            'size', 'founded_year', 'website', 'location', 'description',
            'review_count', 'average_rating', 'is_verified', 'is_active',
            'created_at', 'updated_at'
        )


class CompanyCreateSerializer(serializers.ModelSerializer):
    """公司创建序列化器"""
    
    class Meta:
        model = Company
        fields = (
            'name', 'name_en', 'logo', 'industry', 'size',
            'founded_year', 'website', 'location', 'description'
        )

