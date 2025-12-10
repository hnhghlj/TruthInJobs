from rest_framework import viewsets, filters, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Review, ReviewImage, Comment, CommentImage
from .serializers import (
    ReviewListSerializer,
    ReviewDetailSerializer,
    ReviewCreateSerializer,
    ReviewImageSerializer,
    CommentSerializer,
    CommentCreateSerializer,
    CommentImageSerializer
)
from .permissions import IsOwnerOrReadOnly


class ReviewViewSet(viewsets.ModelViewSet):
    """评价视图集"""
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['company', 'employment_status', 'moderation_status']
    search_fields = ['title', 'content', 'job_title']
    ordering_fields = ['created_at', 'helpful_count', 'view_count', 'overall_rating']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """普通用户只能看到已审核通过的评价，审核员可以看到所有"""
        if self.request.user.is_authenticated and self.request.user.is_moderator():
            return Review.objects.all()
        return Review.objects.filter(moderation_status='approved')
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ReviewListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return ReviewCreateSerializer
        return ReviewDetailSerializer
    
    def retrieve(self, request, *args, **kwargs):
        """查看详情时增加浏览量"""
        instance = self.get_object()
        instance.view_count += 1
        instance.save(update_fields=['view_count'])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def mark_helpful(self, request, pk=None):
        """标记为有用"""
        review = self.get_object()
        review.helpful_count += 1
        review.save(update_fields=['helpful_count'])
        return Response({'message': '操作成功', 'helpful_count': review.helpful_count})
    
    @action(detail=False, methods=['get'])
    def my_reviews(self, request):
        """获取我的评价"""
        if not request.user.is_authenticated:
            return Response({'error': '请先登录'}, status=status.HTTP_401_UNAUTHORIZED)
        
        reviews = Review.objects.filter(user=request.user)
        page = self.paginate_queryset(reviews)
        if page is not None:
            serializer = ReviewListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = ReviewListSerializer(reviews, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def upload_image(self, request, pk=None):
        """上传评价图片"""
        review = self.get_object()
        
        # 检查是否为所有者
        if review.user != request.user:
            return Response({'error': '无权限'}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = ReviewImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(review=review)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentViewSet(viewsets.ModelViewSet):
    """评论视图集"""
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['review', 'parent', 'moderation_status']
    ordering = ['created_at']
    
    def get_queryset(self):
        """普通用户只能看到已审核通过的评论，审核员可以看到所有"""
        if self.request.user.is_authenticated and self.request.user.is_moderator():
            return Comment.objects.all()
        return Comment.objects.filter(moderation_status='approved')
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return CommentCreateSerializer
        return CommentSerializer
    
    @action(detail=True, methods=['post'])
    def mark_helpful(self, request, pk=None):
        """标记为有用"""
        comment = self.get_object()
        comment.helpful_count += 1
        comment.save(update_fields=['helpful_count'])
        return Response({'message': '操作成功', 'helpful_count': comment.helpful_count})
    
    @action(detail=True, methods=['get'])
    def replies(self, request, pk=None):
        """获取评论的回复"""
        comment = self.get_object()
        replies = comment.replies.filter(moderation_status='approved')
        serializer = CommentSerializer(replies, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def upload_image(self, request, pk=None):
        """上传评论图片"""
        comment = self.get_object()
        
        # 检查是否为所有者
        if comment.user != request.user:
            return Response({'error': '无权限'}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = CommentImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(comment=comment)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

