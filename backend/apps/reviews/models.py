from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from apps.companies.models import Company


class Review(models.Model):
    """公司评价"""
    
    MODERATION_STATUS_CHOICES = (
        ('pending', '待审核'),
        ('approved', '已通过'),
        ('rejected', '已拒绝'),
    )
    
    EMPLOYMENT_STATUS_CHOICES = (
        ('current', '在职'),
        ('former', '离职'),
    )
    
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name=_('公司')
    )
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name=_('评价用户')
    )
    
    # 评价内容
    title = models.CharField(_('标题'), max_length=200)
    content = models.TextField(_('评价内容（富文本）'))
    
    # 评分（1-5星）
    overall_rating = models.IntegerField(_('综合评分'), default=5)
    welfare_rating = models.IntegerField(_('福利待遇'), default=5)
    environment_rating = models.IntegerField(_('工作环境'), default=5)
    development_rating = models.IntegerField(_('发展机会'), default=5)
    management_rating = models.IntegerField(_('管理水平'), default=5)
    
    # 职位信息
    job_title = models.CharField(_('职位'), max_length=100, blank=True)
    employment_status = models.CharField(_('就职状态'), max_length=20, choices=EMPLOYMENT_STATUS_CHOICES, default='current')
    work_years = models.IntegerField(_('工作年限'), blank=True, null=True)
    
    # 审核状态
    moderation_status = models.CharField(
        _('审核状态'),
        max_length=20,
        choices=MODERATION_STATUS_CHOICES,
        default='pending',
        db_index=True
    )
    
    # 统计
    helpful_count = models.IntegerField(_('有用数'), default=0)
    comment_count = models.IntegerField(_('评论数'), default=0)
    view_count = models.IntegerField(_('浏览数'), default=0)
    
    # 匿名发布
    is_anonymous = models.BooleanField(_('匿名发布'), default=True)
    
    created_at = models.DateTimeField(_('创建时间'), auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(_('更新时间'), auto_now=True)
    
    class Meta:
        db_table = 'reviews'
        verbose_name = '评价'
        verbose_name_plural = '评价'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['company', 'moderation_status']),
            models.Index(fields=['-created_at']),
        ]
    
    def __str__(self):
        return f"{self.company.name} - {self.title}"
    
    def save(self, *args, **kwargs):
        is_new = self.pk is None
        old_status = None
        
        if not is_new:
            old_review = Review.objects.get(pk=self.pk)
            old_status = old_review.moderation_status
        
        super().save(*args, **kwargs)
        
        # 状态变更为 approved 时更新公司统计
        if old_status != 'approved' and self.moderation_status == 'approved':
            self.company.update_statistics()
            self.user.review_count += 1
            self.user.save(update_fields=['review_count'])


class ReviewImage(models.Model):
    """评价配图"""
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name=_('所属评价')
    )
    image = models.ImageField(_('图片'), upload_to='review_images/')
    caption = models.CharField(_('图片说明'), max_length=200, blank=True)
    order = models.IntegerField(_('排序'), default=0)
    created_at = models.DateTimeField(_('上传时间'), auto_now_add=True)
    
    class Meta:
        db_table = 'review_images'
        verbose_name = '评价图片'
        verbose_name_plural = '评价图片'
        ordering = ['order', 'created_at']
    
    def __str__(self):
        return f"{self.review.title} - 图片{self.order}"


class Comment(models.Model):
    """评论（追加评论）"""
    
    MODERATION_STATUS_CHOICES = (
        ('pending', '待审核'),
        ('approved', '已通过'),
        ('rejected', '已拒绝'),
    )
    
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name=_('所属评价')
    )
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name=_('评论用户')
    )
    
    # 支持回复评论
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='replies',
        verbose_name=_('父评论')
    )
    
    content = models.TextField(_('评论内容'))
    
    # 审核状态
    moderation_status = models.CharField(
        _('审核状态'),
        max_length=20,
        choices=MODERATION_STATUS_CHOICES,
        default='pending',
        db_index=True
    )
    
    # 统计
    helpful_count = models.IntegerField(_('有用数'), default=0)
    
    # 匿名
    is_anonymous = models.BooleanField(_('匿名评论'), default=True)
    
    created_at = models.DateTimeField(_('创建时间'), auto_now_add=True)
    updated_at = models.DateTimeField(_('更新时间'), auto_now=True)
    
    class Meta:
        db_table = 'comments'
        verbose_name = '评论'
        verbose_name_plural = '评论'
        ordering = ['created_at']
    
    def __str__(self):
        return f"评论 on {self.review.title}"
    
    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        
        if is_new and self.moderation_status == 'approved':
            self.review.comment_count += 1
            self.review.save(update_fields=['comment_count'])
            self.user.comment_count += 1
            self.user.save(update_fields=['comment_count'])


class CommentImage(models.Model):
    """评论配图"""
    comment = models.ForeignKey(
        Comment,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name=_('所属评论')
    )
    image = models.ImageField(_('图片'), upload_to='comment_images/')
    order = models.IntegerField(_('排序'), default=0)
    created_at = models.DateTimeField(_('上传时间'), auto_now_add=True)
    
    class Meta:
        db_table = 'comment_images'
        verbose_name = '评论图片'
        verbose_name_plural = '评论图片'
        ordering = ['order', 'created_at']
    
    def __str__(self):
        return f"评论图片{self.order}"

