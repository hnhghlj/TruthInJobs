"""
配置管理模块
提供环境变量读取和验证功能
"""
import os
import sys
from pathlib import Path
from typing import List, Any


def get_env(key: str, default: Any = None, required: bool = False, cast_type: type = str) -> Any:
    """
    获取环境变量
    
    Args:
        key: 环境变量名称
        default: 默认值
        required: 是否必需
        cast_type: 类型转换
        
    Returns:
        环境变量值
        
    Raises:
        ValueError: 当required=True且环境变量不存在时
    """
    value = os.environ.get(key, default)
    
    if required and value is None:
        raise ValueError(f"环境变量 {key} 是必需的，但未设置")
    
    if value is None:
        return default
    
    # 类型转换
    try:
        if cast_type == bool:
            return value.lower() in ('true', '1', 'yes', 'on')
        elif cast_type == int:
            return int(value)
        elif cast_type == float:
            return float(value)
        elif cast_type == list:
            return [item.strip() for item in value.split(',') if item.strip()]
        else:
            return cast_type(value)
    except (ValueError, TypeError) as e:
        raise ValueError(f"无法将环境变量 {key}={value} 转换为 {cast_type.__name__}: {e}")


def validate_config():
    """
    验证配置
    检查必需的环境变量和配置冲突
    """
    errors = []
    warnings = []
    
    # 检查环境
    env = get_env('ENVIRONMENT', 'development')
    
    # 生产环境检查
    if env == 'production':
        # 必须禁用 DEBUG
        if get_env('DEBUG', 'False', cast_type=bool):
            errors.append("生产环境不能启用 DEBUG")
        
        # 必须配置 SECRET_KEY
        secret_key = get_env('SECRET_KEY', '')
        if 'insecure' in secret_key or secret_key == '':
            errors.append("生产环境必须配置安全的 SECRET_KEY")
        
        # 必须配置 ALLOWED_HOSTS
        allowed_hosts = get_env('ALLOWED_HOSTS', '')
        if not allowed_hosts or allowed_hosts == '*':
            errors.append("生产环境必须配置具体的 ALLOWED_HOSTS")
        
        # 建议配置 HTTPS
        if not get_env('SESSION_COOKIE_SECURE', 'False', cast_type=bool):
            warnings.append("生产环境建议启用 HTTPS (SESSION_COOKIE_SECURE=True)")
        
        # 建议配置 Sentry
        if not get_env('SENTRY_DSN', ''):
            warnings.append("生产环境建议配置 Sentry 错误追踪")
    
    # 数据库配置检查
    db_password = get_env('DB_PASSWORD', '')
    if env == 'production' and (not db_password or db_password == 'password'):
        errors.append("生产环境必须配置安全的数据库密码")
    
    # JWT 配置检查
    jwt_secret = get_env('JWT_SECRET_KEY', '')
    if env == 'production' and (not jwt_secret or jwt_secret == get_env('SECRET_KEY', '')):
        warnings.append("建议为 JWT 配置独立的密钥")
    
    # 输出验证结果
    if errors:
        error_msg = "\n" + "="*60 + "\n"
        error_msg += "❌ 配置错误:\n"
        error_msg += "="*60 + "\n"
        for error in errors:
            error_msg += f"  ❌ {error}\n"
        error_msg += "="*60 + "\n"
        
        # 使用 sys.stderr 输出错误，而不是 print
        sys.stderr.write(error_msg)
        sys.exit(1)
    
    if warnings:
        warning_msg = "\n" + "="*60 + "\n"
        warning_msg += "⚠️  配置警告:\n"
        warning_msg += "="*60 + "\n"
        for warning in warnings:
            warning_msg += f"  ⚠️  {warning}\n"
        warning_msg += "="*60 + "\n"
        
        # 使用 sys.stderr 输出警告，而不是 print
        sys.stderr.write(warning_msg)


class Config:
    """配置类，提供统一的配置访问接口"""
    
    # 基本配置
    ENVIRONMENT = get_env('ENVIRONMENT', 'development')
    SECRET_KEY = get_env('SECRET_KEY', 'django-insecure-change-in-production')
    DEBUG = get_env('DEBUG', 'True', cast_type=bool)
    ALLOWED_HOSTS = get_env('ALLOWED_HOSTS', 'localhost,127.0.0.1', cast_type=list)
    
    # 数据库配置
    DB_ENGINE = get_env('DB_ENGINE', 'django.db.backends.mysql')
    DB_NAME = get_env('DB_NAME', 'welfarewatch')
    DB_USER = get_env('DB_USER', 'root')
    DB_PASSWORD = get_env('DB_PASSWORD', 'root')
    DB_HOST = get_env('DB_HOST', 'localhost')
    DB_PORT = get_env('DB_PORT', '3306', cast_type=int)
    DB_CONN_MAX_AGE = get_env('DB_CONN_MAX_AGE', '600', cast_type=int)
    
    # 安全配置
    JWT_SECRET_KEY = get_env('JWT_SECRET_KEY', SECRET_KEY)
    JWT_ALGORITHM = get_env('JWT_ALGORITHM', 'HS256')
    JWT_EXPIRATION_DELTA = get_env('JWT_EXPIRATION_DELTA', '86400', cast_type=int)
    
    SESSION_COOKIE_SECURE = get_env('SESSION_COOKIE_SECURE', 'False', cast_type=bool)
    SESSION_COOKIE_HTTPONLY = get_env('SESSION_COOKIE_HTTPONLY', 'True', cast_type=bool)
    CSRF_COOKIE_SECURE = get_env('CSRF_COOKIE_SECURE', 'False', cast_type=bool)
    
    # CORS 配置
    CORS_ALLOWED_ORIGINS = get_env('CORS_ALLOWED_ORIGINS', 
                                   'http://localhost:5173,http://127.0.0.1:5173',
                                   cast_type=list)
    CORS_ALLOW_CREDENTIALS = get_env('CORS_ALLOW_CREDENTIALS', 'True', cast_type=bool)
    
    # 邮件配置
    EMAIL_BACKEND = get_env('EMAIL_BACKEND', 'django.core.mail.backends.console.EmailBackend')
    EMAIL_HOST = get_env('EMAIL_HOST', 'smtp.gmail.com')
    EMAIL_PORT = get_env('EMAIL_PORT', '587', cast_type=int)
    EMAIL_USE_TLS = get_env('EMAIL_USE_TLS', 'True', cast_type=bool)
    EMAIL_HOST_USER = get_env('EMAIL_HOST_USER', '')
    EMAIL_HOST_PASSWORD = get_env('EMAIL_HOST_PASSWORD', '')
    
    # 管理员配置
    ADMIN_EMAIL = get_env('ADMIN_EMAIL', 'admin@welfarewatch.com')
    ADMIN_NAME = get_env('ADMIN_NAME', 'Admin')
    
    # 缓存配置
    CACHE_BACKEND = get_env('CACHE_BACKEND', 'django.core.cache.backends.locmem.LocMemCache')
    CACHE_LOCATION = get_env('CACHE_LOCATION', 'welfarewatch_cache')
    
    # 日志配置
    LOG_LEVEL = get_env('LOG_LEVEL', 'INFO')
    LOG_DIR = get_env('LOG_DIR', 'logs')
    
    # 性能配置
    RATE_LIMIT_ENABLED = get_env('RATE_LIMIT_ENABLED', 'True', cast_type=bool)
    RATE_LIMIT_PER_MINUTE = get_env('RATE_LIMIT_PER_MINUTE', '60', cast_type=int)
    
    @classmethod
    def is_production(cls) -> bool:
        """是否为生产环境"""
        return cls.ENVIRONMENT == 'production'
    
    @classmethod
    def is_development(cls) -> bool:
        """是否为开发环境"""
        return cls.ENVIRONMENT == 'development'
    
    @classmethod
    def is_staging(cls) -> bool:
        """是否为预发布环境"""
        return cls.ENVIRONMENT == 'staging'


# 在导入时验证配置（仅在非测试环境）
if 'test' not in sys.argv:
    validate_config()

