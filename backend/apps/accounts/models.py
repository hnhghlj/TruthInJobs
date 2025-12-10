from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """自定义用户模型"""
    
    USER_TYPE_CHOICES = (
        ('normal', '普通用户'),
        ('moderator', '审核员'),
        ('admin', '管理员'),
    )
    
    email = models.EmailField(_('邮箱地址'), unique=True)
    phone = models.CharField(_('手机号'), max_length=11, blank=True, null=True)
    user_type = models.CharField(_('用户类型'), max_length=20, choices=USER_TYPE_CHOICES, default='normal')
    avatar = models.ImageField(_('头像'), upload_to='avatars/', blank=True, null=True)
    bio = models.TextField(_('个人简介'), blank=True)
    
    # 匿名标识（用于显示评价）
    anonymous_name = models.CharField(_('匿名昵称'), max_length=50, blank=True)
    
    # 统计信息
    review_count = models.IntegerField(_('评价数'), default=0)
    comment_count = models.IntegerField(_('评论数'), default=0)
    
    created_at = models.DateTimeField(_('创建时间'), auto_now_add=True)
    updated_at = models.DateTimeField(_('更新时间'), auto_now=True)
    
    class Meta:
        db_table = 'users'
        verbose_name = '用户'
        verbose_name_plural = '用户'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.username
    
    def is_moderator(self):
        """是否为审核员"""
        return self.user_type in ['moderator', 'admin']
    
    def is_admin_user(self):
        """是否为管理员"""
        return self.user_type == 'admin' or self.is_superuser

