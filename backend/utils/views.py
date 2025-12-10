"""
工具视图
提供统一的错误处理页面
"""
import logging
from django.http import JsonResponse

logger = logging.getLogger('django.request')


def error_404(request, exception=None):
    """
    404错误处理
    
    Args:
        request: 请求对象
        exception: 异常对象
        
    Returns:
        JsonResponse: 404错误响应
    """
    logger.warning(f"404 Not Found: {request.path}")
    
    return JsonResponse({
        'code': 404,
        'message': '请求的资源不存在',
        'path': request.path
    }, status=404)


def error_500(request):
    """
    500错误处理
    
    Args:
        request: 请求对象
        
    Returns:
        JsonResponse: 500错误响应
    """
    logger.error(f"500 Server Error: {request.path}")
    
    return JsonResponse({
        'code': 500,
        'message': '服务器内部错误',
        'path': request.path
    }, status=500)

