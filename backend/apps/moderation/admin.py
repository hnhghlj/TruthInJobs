from django.contrib import admin
from .models import ModerationLog, Report


@admin.register(ModerationLog)
class ModerationLogAdmin(admin.ModelAdmin):
    list_display = ('content_type', 'object_id', 'moderator', 'action', 'created_at')
    list_filter = ('action', 'content_type', 'created_at')
    search_fields = ('reason', 'moderator__username')
    readonly_fields = ('content_type', 'object_id', 'content_object', 'moderator', 'created_at')


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('content_type', 'object_id', 'reporter', 'report_type', 'status', 'handler', 'created_at')
    list_filter = ('report_type', 'status', 'created_at')
    search_fields = ('description', 'reporter__username', 'handler__username')
    readonly_fields = ('content_type', 'object_id', 'content_object', 'reporter', 'created_at', 'updated_at')
    
    fieldsets = (
        ('举报信息', {
            'fields': ('content_type', 'object_id', 'content_object', 'reporter', 'report_type', 'description')
        }),
        ('处理信息', {
            'fields': ('status', 'handler', 'handler_note', 'handled_at')
        }),
        ('时间信息', {
            'fields': ('created_at', 'updated_at')
        }),
    )

