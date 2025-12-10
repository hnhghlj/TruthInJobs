"""
自定义装饰器
提供各种功能装饰器
"""
import logging
import time
from functools import wraps
from django.core.cache import cache
from django.utils.decorators import method_decorator
from rest_framework import status
from .responses import APIResponse

logger = logging.getLogger('django')


def log_execution_time(func):
    """
    记录函数执行时间的装饰器
    
    Usage:
        @log_execution_time
        def my_function():
            pass
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        
        try:
            result = func(*args, **kwargs)
            duration = time.time() - start_time
            
            logger.info(
                f"Function {func.__module__}.{func.__name__} "
                f"executed in {duration:.2f}s"
            )
            
            # 慢查询警告
            if duration > 1.0:
                logger.warning(
                    f"Slow function detected: {func.__name__} "
                    f"took {duration:.2f}s"
                )
            
            return result
        except Exception as e:
            duration = time.time() - start_time
            logger.error(
                f"Function {func.__module__}.{func.__name__} "
                f"failed after {duration:.2f}s: {e}",
                exc_info=True
            )
            raise
    
    return wrapper


def cache_response(timeout=300, key_prefix=''):
    """
    缓存响应装饰器
    
    Args:
        timeout: 缓存时间（秒）
        key_prefix: 缓存键前缀
        
    Usage:
        @cache_response(timeout=600, key_prefix='company_list')
        def list(self, request):
            pass
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # 生成缓存键
            request = None
            for arg in args:
                if hasattr(arg, 'query_params'):
                    request = arg
                    break
            
            if not request:
                return func(*args, **kwargs)
            
            # 构建缓存键
            cache_key = f"{key_prefix}:{request.path}:{request.query_params.urlencode()}"
            
            # 尝试从缓存获取
            cached_response = cache.get(cache_key)
            if cached_response:
                logger.debug(f"Cache hit: {cache_key}")
                return cached_response
            
            # 执行函数
            response = func(*args, **kwargs)
            
            # 缓存响应
            if response.status_code == 200:
                cache.set(cache_key, response, timeout)
                logger.debug(f"Cache set: {cache_key} (timeout={timeout}s)")
            
            return response
        
        return wrapper
    return decorator


def require_moderator(func):
    """
    要求审核员权限的装饰器
    
    Usage:
        @require_moderator
        def moderate_review(self, request):
            pass
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        request = None
        for arg in args:
            if hasattr(arg, 'user'):
                request = arg
                break
        
        if not request:
            return APIResponse.error(message="Invalid request")
        
        if not request.user.is_authenticated:
            logger.warning(f"Unauthenticated user tried to access moderator endpoint")
            return APIResponse.unauthorized()
        
        if not request.user.is_moderator():
            logger.warning(
                f"User {request.user.id} ({request.user.username}) "
                f"attempted to access moderator endpoint without permission"
            )
            return APIResponse.forbidden(message="需要审核员权限")
        
        return func(*args, **kwargs)
    
    return wrapper


def require_admin(func):
    """
    要求管理员权限的装饰器
    
    Usage:
        @require_admin
        def admin_action(self, request):
            pass
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        request = None
        for arg in args:
            if hasattr(arg, 'user'):
                request = arg
                break
        
        if not request:
            return APIResponse.error(message="Invalid request")
        
        if not request.user.is_authenticated:
            return APIResponse.unauthorized()
        
        if not request.user.is_admin_user():
            logger.warning(
                f"User {request.user.id} ({request.user.username}) "
                f"attempted to access admin endpoint without permission"
            )
            return APIResponse.forbidden(message="需要管理员权限")
        
        return func(*args, **kwargs)
    
    return wrapper


def validate_request_data(required_fields):
    """
    验证请求数据的装饰器
    
    Args:
        required_fields: 必需字段列表
        
    Usage:
        @validate_request_data(['username', 'password'])
        def login(self, request):
            pass
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            request = None
            for arg in args:
                if hasattr(arg, 'data'):
                    request = arg
                    break
            
            if not request:
                return APIResponse.error(message="Invalid request")
            
            missing_fields = []
            for field in required_fields:
                if field not in request.data or not request.data[field]:
                    missing_fields.append(field)
            
            if missing_fields:
                logger.warning(f"Missing required fields: {missing_fields}")
                return APIResponse.validation_error(
                    errors={'missing_fields': missing_fields},
                    message=f"缺少必需字段: {', '.join(missing_fields)}"
                )
            
            return func(*args, **kwargs)
        
        return wrapper
    return decorator


def transaction_atomic_with_logging(func):
    """
    带日志的数据库事务装饰器
    
    Usage:
        @transaction_atomic_with_logging
        def update_data(self):
            pass
    """
    from django.db import transaction
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger.debug(f"Starting transaction: {func.__name__}")
        
        try:
            with transaction.atomic():
                result = func(*args, **kwargs)
                logger.info(f"Transaction committed: {func.__name__}")
                return result
        except Exception as e:
            logger.error(
                f"Transaction rolled back: {func.__name__}, error: {e}",
                exc_info=True
            )
            raise
    
    return wrapper

