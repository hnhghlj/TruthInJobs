from django.contrib import admin
from .models import Industry, Company


@admin.register(Industry)
class IndustryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'industry', 'size', 'review_count', 'average_rating', 'is_verified', 'is_active', 'created_at')
    list_filter = ('industry', 'size', 'is_verified', 'is_active', 'created_at')
    search_fields = ('name', 'name_en', 'location')
    readonly_fields = ('review_count', 'average_rating', 'created_at', 'updated_at')
    
    fieldsets = (
        ('基本信息', {
            'fields': ('name', 'name_en', 'logo', 'industry', 'size', 'founded_year')
        }),
        ('详细信息', {
            'fields': ('website', 'location', 'description')
        }),
        ('统计信息', {
            'fields': ('review_count', 'average_rating')
        }),
        ('状态', {
            'fields': ('is_verified', 'is_active')
        }),
        ('时间信息', {
            'fields': ('created_at', 'updated_at')
        }),
    )

