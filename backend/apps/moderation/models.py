from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext_lazy as _


class ModerationLog(models.Model):
    """审核日志"""
    
    ACTION_CHOICES = (
        ('approve', '通过'),
        ('reject', '拒绝'),
        ('pending', '待审核'),
    )
    
    # 使用 GenericForeignKey 支持多种内容类型
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        verbose_name=_('内容类型')
    )
    object_id = models.PositiveIntegerField(_('对象ID'))
    content_object = GenericForeignKey('content_type', 'object_id')
    
    # 审核员
    moderator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='moderation_logs',
        verbose_name=_('审核员')
    )
    
    action = models.CharField(_('审核动作'), max_length=20, choices=ACTION_CHOICES)
    reason = models.TextField(_('审核原因/备注'), blank=True)
    
    created_at = models.DateTimeField(_('审核时间'), auto_now_add=True)
    
    class Meta:
        db_table = 'moderation_logs'
        verbose_name = '审核日志'
        verbose_name_plural = '审核日志'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.get_action_display()} - {self.content_type} #{self.object_id}"


class Report(models.Model):
    """举报"""
    
    REPORT_TYPE_CHOICES = (
        ('spam', '垃圾信息'),
        ('inappropriate', '不当内容'),
        ('false_info', '虚假信息'),
        ('offensive', '攻击性言论'),
        ('other', '其他'),
    )
    
    STATUS_CHOICES = (
        ('pending', '待处理'),
        ('processing', '处理中'),
        ('resolved', '已处理'),
        ('dismissed', '已驳回'),
    )
    
    # 使用 GenericForeignKey 支持举报多种内容
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        verbose_name=_('举报内容类型')
    )
    object_id = models.PositiveIntegerField(_('对象ID'))
    content_object = GenericForeignKey('content_type', 'object_id')
    
    # 举报人
    reporter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reports',
        verbose_name=_('举报人')
    )
    
    report_type = models.CharField(_('举报类型'), max_length=20, choices=REPORT_TYPE_CHOICES)
    description = models.TextField(_('举报说明'))
    
    status = models.CharField(_('处理状态'), max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # 处理信息
    handler = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='handled_reports',
        verbose_name=_('处理人')
    )
    handler_note = models.TextField(_('处理备注'), blank=True)
    handled_at = models.DateTimeField(_('处理时间'), null=True, blank=True)
    
    created_at = models.DateTimeField(_('举报时间'), auto_now_add=True)
    updated_at = models.DateTimeField(_('更新时间'), auto_now=True)
    
    class Meta:
        db_table = 'reports'
        verbose_name = '举报'
        verbose_name_plural = '举报'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.get_report_type_display()} - {self.content_type}"

