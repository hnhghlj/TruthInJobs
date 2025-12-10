from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from .models import ModerationLog, Report
from .serializers import ModerationLogSerializer, ReportSerializer, ReportCreateSerializer
from apps.reviews.permissions import IsModerator
from apps.reviews.models import Review, Comment


class ModerationLogViewSet(viewsets.ReadOnlyModelViewSet):
    """审核日志视图集（只读）"""
    queryset = ModerationLog.objects.all()
    serializer_class = ModerationLogSerializer
    permission_classes = [IsModerator]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['content_type', 'action', 'moderator']
    ordering = ['-created_at']


class ReportViewSet(viewsets.ModelViewSet):
    """举报视图集"""
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['report_type', 'status', 'content_type']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """普通用户只能看到自己的举报，审核员可以看到所有"""
        if self.request.user.is_moderator():
            return Report.objects.all()
        return Report.objects.filter(reporter=self.request.user)
    
    def get_serializer_class(self):
        if self.action == 'create':
            return ReportCreateSerializer
        return ReportSerializer
    
    @action(detail=True, methods=['post'], permission_classes=[IsModerator])
    def handle(self, request, pk=None):
        """处理举报"""
        report = self.get_object()
        
        action_type = request.data.get('action')  # 'resolve' or 'dismiss'
        handler_note = request.data.get('handler_note', '')
        
        if action_type == 'resolve':
            report.status = 'resolved'
        elif action_type == 'dismiss':
            report.status = 'dismissed'
        else:
            return Response({'error': '无效的操作'}, status=status.HTTP_400_BAD_REQUEST)
        
        report.handler = request.user
        report.handler_note = handler_note
        report.handled_at = timezone.now()
        report.save()
        
        serializer = self.get_serializer(report)
        return Response(serializer.data)


class ModerationViewSet(viewsets.ViewSet):
    """审核视图集"""
    permission_classes = [IsModerator]
    
    @action(detail=False, methods=['get'])
    def pending_reviews(self, request):
        """获取待审核的评价"""
        from apps.reviews.serializers import ReviewListSerializer
        
        reviews = Review.objects.filter(moderation_status='pending').order_by('-created_at')
        serializer = ReviewListSerializer(reviews, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def pending_comments(self, request):
        """获取待审核的评论"""
        from apps.reviews.serializers import CommentSerializer
        
        comments = Comment.objects.filter(moderation_status='pending').order_by('-created_at')
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def moderate_review(self, request):
        """审核评价"""
        review_id = request.data.get('review_id')
        action_type = request.data.get('action')  # 'approve' or 'reject'
        reason = request.data.get('reason', '')
        
        try:
            review = Review.objects.get(id=review_id)
        except Review.DoesNotExist:
            return Response({'error': '评价不存在'}, status=status.HTTP_404_NOT_FOUND)
        
        if action_type == 'approve':
            review.moderation_status = 'approved'
        elif action_type == 'reject':
            review.moderation_status = 'rejected'
        else:
            return Response({'error': '无效的操作'}, status=status.HTTP_400_BAD_REQUEST)
        
        review.save()
        
        # 记录审核日志
        ModerationLog.objects.create(
            content_type=ContentType.objects.get_for_model(Review),
            object_id=review.id,
            moderator=request.user,
            action=action_type,
            reason=reason
        )
        
        from apps.reviews.serializers import ReviewDetailSerializer
        serializer = ReviewDetailSerializer(review)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def moderate_comment(self, request):
        """审核评论"""
        comment_id = request.data.get('comment_id')
        action_type = request.data.get('action')  # 'approve' or 'reject'
        reason = request.data.get('reason', '')
        
        try:
            comment = Comment.objects.get(id=comment_id)
        except Comment.DoesNotExist:
            return Response({'error': '评论不存在'}, status=status.HTTP_404_NOT_FOUND)
        
        if action_type == 'approve':
            comment.moderation_status = 'approved'
        elif action_type == 'reject':
            comment.moderation_status = 'rejected'
        else:
            return Response({'error': '无效的操作'}, status=status.HTTP_400_BAD_REQUEST)
        
        comment.save()
        
        # 记录审核日志
        ModerationLog.objects.create(
            content_type=ContentType.objects.get_for_model(Comment),
            object_id=comment.id,
            moderator=request.user,
            action=action_type,
            reason=reason
        )
        
        from apps.reviews.serializers import CommentSerializer
        serializer = CommentSerializer(comment)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """获取审核统计信息"""
        stats = {
            'pending_reviews': Review.objects.filter(moderation_status='pending').count(),
            'pending_comments': Comment.objects.filter(moderation_status='pending').count(),
            'pending_reports': Report.objects.filter(status='pending').count(),
            'approved_reviews_today': Review.objects.filter(
                moderation_status='approved',
                updated_at__date=timezone.now().date()
            ).count(),
            'approved_comments_today': Comment.objects.filter(
                moderation_status='approved',
                updated_at__date=timezone.now().date()
            ).count(),
        }
        return Response(stats)

