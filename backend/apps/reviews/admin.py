from django.contrib import admin
from .models import Review, ReviewImage, Comment, CommentImage


class ReviewImageInline(admin.TabularInline):
    model = ReviewImage
    extra = 1


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'user', 'overall_rating', 'moderation_status', 'is_anonymous', 'view_count', 'created_at')
    list_filter = ('moderation_status', 'employment_status', 'is_anonymous', 'created_at')
    search_fields = ('title', 'content', 'company__name', 'user__username')
    readonly_fields = ('helpful_count', 'comment_count', 'view_count', 'created_at', 'updated_at')
    inlines = [ReviewImageInline]
    
    fieldsets = (
        ('基本信息', {
            'fields': ('company', 'user', 'title', 'content')
        }),
        ('评分', {
            'fields': ('overall_rating', 'welfare_rating', 'environment_rating', 'development_rating', 'management_rating')
        }),
        ('职位信息', {
            'fields': ('job_title', 'employment_status', 'work_years')
        }),
        ('审核', {
            'fields': ('moderation_status',)
        }),
        ('设置', {
            'fields': ('is_anonymous',)
        }),
        ('统计', {
            'fields': ('helpful_count', 'comment_count', 'view_count')
        }),
        ('时间', {
            'fields': ('created_at', 'updated_at')
        }),
    )


class CommentImageInline(admin.TabularInline):
    model = CommentImage
    extra = 1


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('review', 'user', 'content_preview', 'moderation_status', 'is_anonymous', 'created_at')
    list_filter = ('moderation_status', 'is_anonymous', 'created_at')
    search_fields = ('content', 'user__username')
    readonly_fields = ('helpful_count', 'created_at', 'updated_at')
    inlines = [CommentImageInline]
    
    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = '内容预览'


@admin.register(ReviewImage)
class ReviewImageAdmin(admin.ModelAdmin):
    list_display = ('review', 'caption', 'order', 'created_at')
    list_filter = ('created_at',)


@admin.register(CommentImage)
class CommentImageAdmin(admin.ModelAdmin):
    list_display = ('comment', 'order', 'created_at')
    list_filter = ('created_at',)

