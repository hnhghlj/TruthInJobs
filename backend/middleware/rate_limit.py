"""
API 限流中间件
防止恶意请求和DDoS攻击
"""
import logging
import time
from django.core.cache import cache
from django.http import JsonResponse
from django.conf import settings
from config import Config

logger = logging.getLogger('django.security')


class RateLimitMiddleware:
    """
    基于IP的API限流中间件
    使用缓存存储请求次数
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        from django.conf import settings
        # 开发环境禁用限流
        self.enabled = Config.RATE_LIMIT_ENABLED and not settings.DEBUG
        self.rate_limit = Config.RATE_LIMIT_PER_MINUTE
    
    def __call__(self, request):
        # 如果未启用限流，直接通过
        if not self.enabled:
            return self.get_response(request)
        
        # 只对API请求限流
        if not request.path.startswith('/api/'):
            return self.get_response(request)
        
        # 获取客户端IP
        ip_address = self.get_client_ip(request)
        
        # 检查是否超过限流
        if self.is_rate_limited(ip_address):
            logger.warning(
                f"Rate limit exceeded for IP: {ip_address}, "
                f"path: {request.path}, method: {request.method}"
            )
            return JsonResponse({
                'error': '请求过于频繁，请稍后再试',
                'detail': f'每分钟最多 {self.rate_limit} 次请求'
            }, status=429)
        
        response = self.get_response(request)
        return response
    
    def get_client_ip(self, request) -> str:
        """获取客户端真实IP"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR', '')
        return ip
    
    def is_rate_limited(self, ip_address: str) -> bool:
        """
        检查是否超过限流
        
        Args:
            ip_address: 客户端IP地址
            
        Returns:
            bool: 是否被限流
        """
        cache_key = f'rate_limit:{ip_address}'
        
        # 获取当前请求次数
        request_count = cache.get(cache_key, 0)
        
        if request_count >= self.rate_limit:
            return True
        
        # 增加请求次数
        cache.set(cache_key, request_count + 1, 60)  # 60秒过期
        
        return False


class RequestLoggingMiddleware:
    """
    请求日志中间件
    记录所有API请求的详细信息
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        self.logger = logging.getLogger('django.request')
    
    def __call__(self, request):
        # 记录请求开始时间
        start_time = time.time()
        
        # 记录请求信息
        self.logger.info(
            f"Request started: {request.method} {request.path} "
            f"from {self.get_client_ip(request)}"
        )
        
        # 处理请求
        response = self.get_response(request)
        
        # 计算请求处理时间
        duration = time.time() - start_time
        
        # 记录响应信息
        self.logger.info(
            f"Request completed: {request.method} {request.path} "
            f"status={response.status_code} duration={duration:.2f}s"
        )
        
        # 如果请求时间过长，记录警告
        if duration > 1.0:
            self.logger.warning(
                f"Slow request detected: {request.method} {request.path} "
                f"took {duration:.2f}s"
            )
        
        return response
    
    def get_client_ip(self, request) -> str:
        """获取客户端真实IP"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR', '')
        return ip


class SecurityHeadersMiddleware:
    """
    安全头中间件
    添加各种安全相关的HTTP头
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        response = self.get_response(request)
        
        # 添加安全头
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['X-XSS-Protection'] = '1; mode=block'
        
        # 生产环境添加更多安全头
        if Config.is_production():
            response['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
            response['Content-Security-Policy'] = "default-src 'self'"
        
        return response

