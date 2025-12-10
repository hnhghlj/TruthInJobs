"""
全局异常处理
统一处理各种异常，返回标准格式的错误响应
"""
import logging
from django.core.exceptions import ValidationError as DjangoValidationError
from django.http import Http404
from rest_framework import exceptions
from rest_framework.views import exception_handler as drf_exception_handler
from rest_framework import status
from .responses import APIResponse

logger = logging.getLogger('django.request')


def custom_exception_handler(exc, context):
    """
    自定义异常处理器
    
    Args:
        exc: 异常对象
        context: 上下文信息
        
    Returns:
        Response: 错误响应
    """
    # 调用DRF默认的异常处理器
    response = drf_exception_handler(exc, context)
    
    # 获取请求信息
    request = context.get('request')
    view = context.get('view')
    
    # 记录异常日志
    logger.error(
        f"Exception in {view.__class__.__name__ if view else 'Unknown'}: "
        f"{exc.__class__.__name__}: {str(exc)}",
        exc_info=True,
        extra={
            'request': request,
            'view': view,
        }
    )
    
    # 如果DRF已经处理了异常
    if response is not None:
        # 统一响应格式
        error_data = {
            'code': response.status_code,
            'message': get_error_message(exc),
        }
        
        # 添加详细错误信息
        if isinstance(response.data, dict):
            if 'detail' in response.data:
                error_data['message'] = response.data['detail']
            else:
                error_data['errors'] = response.data
        elif isinstance(response.data, list):
            error_data['errors'] = response.data
        
        response.data = error_data
        return response
    
    # 处理Django的404异常
    if isinstance(exc, Http404):
        return APIResponse.not_found(message="资源不存在")
    
    # 处理Django的验证异常
    if isinstance(exc, DjangoValidationError):
        return APIResponse.validation_error(
            errors={'detail': list(exc.messages)},
            message="数据验证失败"
        )
    
    # 处理其他未捕获的异常
    logger.critical(
        f"Unhandled exception: {exc.__class__.__name__}: {str(exc)}",
        exc_info=True
    )
    
    # 生产环境返回通用错误信息
    from config import Config
    if Config.is_production():
        return APIResponse.server_error(message="服务器内部错误，请稍后重试")
    else:
        # 开发环境返回详细错误信息
        return APIResponse.server_error(
            message=f"{exc.__class__.__name__}: {str(exc)}"
        )


def get_error_message(exc) -> str:
    """
    获取友好的错误消息
    
    Args:
        exc: 异常对象
        
    Returns:
        str: 错误消息
    """
    if isinstance(exc, exceptions.AuthenticationFailed):
        return "认证失败，请重新登录"
    elif isinstance(exc, exceptions.NotAuthenticated):
        return "请先登录"
    elif isinstance(exc, exceptions.PermissionDenied):
        return "没有权限执行此操作"
    elif isinstance(exc, exceptions.NotFound):
        return "请求的资源不存在"
    elif isinstance(exc, exceptions.ValidationError):
        return "数据验证失败"
    elif isinstance(exc, exceptions.MethodNotAllowed):
        return "不支持的请求方法"
    elif isinstance(exc, exceptions.Throttled):
        wait = exc.wait
        return f"请求过于频繁，请在 {wait} 秒后重试"
    else:
        return str(exc)


class BusinessException(Exception):
    """
    业务异常基类
    用于业务逻辑中的自定义异常
    """
    
    def __init__(
        self,
        message: str = "业务处理失败",
        code: int = status.HTTP_400_BAD_REQUEST,
        errors: dict = None
    ):
        self.message = message
        self.code = code
        self.errors = errors or {}
        super().__init__(message)


class ResourceNotFoundException(BusinessException):
    """资源不存在异常"""
    
    def __init__(self, message: str = "资源不存在"):
        super().__init__(message, status.HTTP_404_NOT_FOUND)


class PermissionDeniedException(BusinessException):
    """权限不足异常"""
    
    def __init__(self, message: str = "没有权限执行此操作"):
        super().__init__(message, status.HTTP_403_FORBIDDEN)


class ValidationException(BusinessException):
    """验证失败异常"""
    
    def __init__(self, message: str = "数据验证失败", errors: dict = None):
        super().__init__(message, status.HTTP_400_BAD_REQUEST, errors)

