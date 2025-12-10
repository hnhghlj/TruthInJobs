from rest_framework import serializers
from .models import ModerationLog, Report
from apps.reviews.serializers import ReviewListSerializer, CommentSerializer


class ModerationLogSerializer(serializers.ModelSerializer):
    """审核日志序列化器"""
    moderator_name = serializers.CharField(source='moderator.username', read_only=True)
    content_type_name = serializers.CharField(source='content_type.model', read_only=True)
    
    class Meta:
        model = ModerationLog
        fields = (
            'id', 'content_type', 'content_type_name', 'object_id',
            'moderator', 'moderator_name', 'action', 'reason', 'created_at'
        )
        read_only_fields = ('id', 'created_at')


class ReportSerializer(serializers.ModelSerializer):
    """举报序列化器"""
    reporter_name = serializers.CharField(source='reporter.username', read_only=True)
    handler_name = serializers.CharField(source='handler.username', read_only=True, allow_null=True)
    content_type_name = serializers.CharField(source='content_type.model', read_only=True)
    
    class Meta:
        model = Report
        fields = (
            'id', 'content_type', 'content_type_name', 'object_id',
            'reporter', 'reporter_name', 'report_type', 'description',
            'status', 'handler', 'handler_name', 'handler_note', 'handled_at',
            'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'reporter', 'handler', 'handled_at', 'created_at', 'updated_at')


class ReportCreateSerializer(serializers.ModelSerializer):
    """举报创建序列化器"""
    
    class Meta:
        model = Report
        fields = ('content_type', 'object_id', 'report_type', 'description')
    
    def create(self, validated_data):
        validated_data['reporter'] = self.context['request'].user
        return super().create(validated_data)

