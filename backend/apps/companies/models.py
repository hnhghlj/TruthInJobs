from django.db import models
from django.utils.translation import gettext_lazy as _


class Industry(models.Model):
    """行业分类"""
    name = models.CharField(_('行业名称'), max_length=100, unique=True)
    description = models.TextField(_('行业描述'), blank=True)
    created_at = models.DateTimeField(_('创建时间'), auto_now_add=True)
    
    class Meta:
        db_table = 'industries'
        verbose_name = '行业'
        verbose_name_plural = '行业'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Company(models.Model):
    """公司信息"""
    
    COMPANY_SIZE_CHOICES = (
        ('1-50', '1-50人'),
        ('51-200', '51-200人'),
        ('201-500', '201-500人'),
        ('501-1000', '501-1000人'),
        ('1001-5000', '1001-5000人'),
        ('5001+', '5000人以上'),
    )
    
    name = models.CharField(_('公司名称'), max_length=200, unique=True, db_index=True)
    name_en = models.CharField(_('英文名称'), max_length=200, blank=True)
    logo = models.ImageField(_('公司Logo'), upload_to='company_logos/', blank=True, null=True)
    
    industry = models.ForeignKey(
        Industry,
        on_delete=models.SET_NULL,
        null=True,
        related_name='companies',
        verbose_name=_('所属行业')
    )
    
    size = models.CharField(_('公司规模'), max_length=20, choices=COMPANY_SIZE_CHOICES, blank=True)
    founded_year = models.IntegerField(_('成立年份'), blank=True, null=True)
    
    website = models.URLField(_('官方网站'), blank=True)
    location = models.CharField(_('总部地址'), max_length=200, blank=True)
    
    description = models.TextField(_('公司简介'), blank=True)
    
    # 统计信息
    review_count = models.IntegerField(_('评价数'), default=0)
    average_rating = models.DecimalField(_('平均评分'), max_digits=3, decimal_places=2, default=0)
    
    # 状态
    is_verified = models.BooleanField(_('已认证'), default=False)
    is_active = models.BooleanField(_('激活状态'), default=True)
    
    created_at = models.DateTimeField(_('创建时间'), auto_now_add=True)
    updated_at = models.DateTimeField(_('更新时间'), auto_now=True)
    
    class Meta:
        db_table = 'companies'
        verbose_name = '公司'
        verbose_name_plural = '公司'
        ordering = ['-review_count', 'name']
    
    def __str__(self):
        return self.name
    
    def update_statistics(self):
        """更新统计信息"""
        from apps.reviews.models import Review
        approved_reviews = Review.objects.filter(
            company=self,
            moderation_status='approved'
        )
        self.review_count = approved_reviews.count()
        if self.review_count > 0:
            avg = approved_reviews.aggregate(models.Avg('overall_rating'))['overall_rating__avg']
            self.average_rating = round(avg, 2) if avg else 0
        else:
            self.average_rating = 0
        self.save(update_fields=['review_count', 'average_rating'])

