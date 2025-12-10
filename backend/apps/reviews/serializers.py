from rest_framework import serializers
from .models import Review, ReviewImage, Comment, CommentImage
from apps.accounts.serializers import UserSerializer


class ReviewImageSerializer(serializers.ModelSerializer):
    """评价图片序列化器"""
    
    class Meta:
        model = ReviewImage
        fields = ('id', 'image', 'caption', 'order', 'created_at')
        read_only_fields = ('id', 'created_at')


class CommentImageSerializer(serializers.ModelSerializer):
    """评论图片序列化器"""
    
    class Meta:
        model = CommentImage
        fields = ('id', 'image', 'order', 'created_at')
        read_only_fields = ('id', 'created_at')


class CommentSerializer(serializers.ModelSerializer):
    """评论序列化器"""
    user_info = serializers.SerializerMethodField()
    images = CommentImageSerializer(many=True, read_only=True)
    reply_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Comment
        fields = (
            'id', 'review', 'user', 'user_info', 'parent', 'content',
            'moderation_status', 'helpful_count', 'is_anonymous',
            'images', 'reply_count', 'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'user', 'moderation_status', 'helpful_count', 'created_at', 'updated_at')
    
    def get_user_info(self, obj):
        """获取用户信息（考虑匿名）"""
        if obj.is_anonymous:
            return {
                'username': obj.user.anonymous_name or '匿名用户',
                'is_anonymous': True
            }
        return {
            'id': obj.user.id,
            'username': obj.user.username,
            'avatar': obj.user.avatar.url if obj.user.avatar else None,
            'is_anonymous': False
        }
    
    def get_reply_count(self, obj):
        """获取回复数量"""
        return obj.replies.filter(moderation_status='approved').count()


class ReviewListSerializer(serializers.ModelSerializer):
    """评价列表序列化器"""
    company_name = serializers.CharField(source='company.name', read_only=True)
    user_info = serializers.SerializerMethodField()
    
    class Meta:
        model = Review
        fields = (
            'id', 'company', 'company_name', 'user_info', 'title',
            'overall_rating', 'welfare_rating', 'environment_rating',
            'development_rating', 'management_rating',
            'job_title', 'employment_status',
            'moderation_status', 'helpful_count', 'comment_count', 'view_count',
            'is_anonymous', 'created_at'
        )
    
    def get_user_info(self, obj):
        """获取用户信息（考虑匿名）"""
        if obj.is_anonymous:
            return {
                'username': obj.user.anonymous_name or '匿名用户',
                'is_anonymous': True
            }
        return {
            'id': obj.user.id,
            'username': obj.user.username,
            'avatar': obj.user.avatar.url if obj.user.avatar else None,
            'is_anonymous': False
        }


class ReviewDetailSerializer(serializers.ModelSerializer):
    """评价详情序列化器"""
    company_name = serializers.CharField(source='company.name', read_only=True)
    user_info = serializers.SerializerMethodField()
    images = ReviewImageSerializer(many=True, read_only=True)
    comments = serializers.SerializerMethodField()
    
    class Meta:
        model = Review
        fields = (
            'id', 'company', 'company_name', 'user', 'user_info',
            'title', 'content',
            'overall_rating', 'welfare_rating', 'environment_rating',
            'development_rating', 'management_rating',
            'job_title', 'employment_status', 'work_years',
            'moderation_status', 'helpful_count', 'comment_count', 'view_count',
            'is_anonymous', 'images', 'comments',
            'created_at', 'updated_at'
        )
        read_only_fields = (
            'id', 'user', 'moderation_status', 
            'helpful_count', 'comment_count', 'view_count',
            'created_at', 'updated_at'
        )
    
    def get_user_info(self, obj):
        """获取用户信息（考虑匿名）"""
        if obj.is_anonymous:
            return {
                'username': obj.user.anonymous_name or '匿名用户',
                'is_anonymous': True
            }
        return {
            'id': obj.user.id,
            'username': obj.user.username,
            'avatar': obj.user.avatar.url if obj.user.avatar else None,
            'is_anonymous': False
        }
    
    def get_comments(self, obj):
        """获取已审核通过的评论"""
        comments = obj.comments.filter(
            moderation_status='approved',
            parent__isnull=True  # 只获取顶级评论
        )
        return CommentSerializer(comments, many=True).data


class ReviewCreateSerializer(serializers.ModelSerializer):
    """评价创建序列化器"""
    
    class Meta:
        model = Review
        fields = (
            'company', 'title', 'content',
            'overall_rating', 'welfare_rating', 'environment_rating',
            'development_rating', 'management_rating',
            'job_title', 'employment_status', 'work_years',
            'is_anonymous'
        )
    
    def validate(self, data):
        """验证评分范围"""
        rating_fields = [
            'overall_rating', 'welfare_rating', 'environment_rating',
            'development_rating', 'management_rating'
        ]
        for field in rating_fields:
            if field in data and (data[field] < 1 or data[field] > 5):
                raise serializers.ValidationError(f"{field} 必须在 1-5 之间")
        return data
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class CommentCreateSerializer(serializers.ModelSerializer):
    """评论创建序列化器"""
    
    class Meta:
        model = Comment
        fields = ('review', 'parent', 'content', 'is_anonymous')
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

