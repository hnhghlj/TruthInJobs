"""
Django settings for welfare_watch project.
企业级配置 - 使用环境变量管理
"""

from pathlib import Path
import os
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# 确保日志目录存在（必须在导入 config 之前）
LOGS_DIR = BASE_DIR / 'logs'
if not LOGS_DIR.exists():
    LOGS_DIR.mkdir(parents=True, exist_ok=True)

# 加载环境变量
env_file = BASE_DIR / '.env'
if env_file.exists():
    load_dotenv(env_file)

# 导入配置模块
from config import Config

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = Config.SECRET_KEY

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = Config.DEBUG

# 允许的主机（生产环境必须配置）
ALLOWED_HOSTS = Config.ALLOWED_HOSTS


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third party apps
    'rest_framework',
    'corsheaders',
    'django_filters',
    'ckeditor',
    'ckeditor_uploader',
    'drf_spectacular',
    
    # Local apps
    'apps.accounts',
    'apps.companies',
    'apps.reviews',
    'apps.moderation',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 自定义中间件
    'middleware.rate_limit.RateLimitMiddleware',
    'middleware.rate_limit.RequestLoggingMiddleware',
    'middleware.rate_limit.SecurityHeadersMiddleware',
]

ROOT_URLCONF = 'welfare_watch.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'welfare_watch.wsgi.application'


# Database
# MySQL 配置（从环境变量读取）
DATABASES = {
    'default': {
        'ENGINE': Config.DB_ENGINE,
        'NAME': Config.DB_NAME,
        'USER': Config.DB_USER,
        'PASSWORD': Config.DB_PASSWORD,
        'HOST': Config.DB_HOST,
        'PORT': Config.DB_PORT,
        'CONN_MAX_AGE': Config.DB_CONN_MAX_AGE,
        'OPTIONS': {
            'charset': 'utf8mb4',
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES',time_zone='+08:00'",
        },
    }
}

# 开发环境可以使用 SQLite（可选）
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Custom User Model
AUTH_USER_MODEL = 'accounts.User'

# REST Framework settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'apps.accounts.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    # 全局异常处理
    'EXCEPTION_HANDLER': 'utils.exceptions.custom_exception_handler',
    # 默认渲染器
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    # 开发环境添加浏览器API
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ] if DEBUG else [
        'rest_framework.renderers.JSONRenderer',
    ],
    # 限流配置
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/hour',  # 匿名用户每小时100次
        'user': '1000/hour',  # 认证用户每小时1000次
    },
}

# CORS settings（从环境变量读取）
CORS_ALLOWED_ORIGINS = Config.CORS_ALLOWED_ORIGINS
CORS_ALLOW_CREDENTIALS = Config.CORS_ALLOW_CREDENTIALS

# 安全设置（生产环境）
if Config.is_production():
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'
    
# Session 配置
SESSION_COOKIE_HTTPONLY = Config.SESSION_COOKIE_HTTPONLY
SESSION_COOKIE_SECURE = Config.SESSION_COOKIE_SECURE
SESSION_COOKIE_AGE = 1209600  # 2 weeks

# CSRF 配置  
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SECURE = Config.CSRF_COOKIE_SECURE
if not DEBUG:
    CSRF_TRUSTED_ORIGINS = Config.CORS_ALLOWED_ORIGINS

# CKEditor settings
CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_IMAGE_BACKEND = "pillow"
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
        'height': 300,
        'width': '100%',
    },
}

# JWT settings（从环境变量读取）
JWT_SECRET_KEY = Config.JWT_SECRET_KEY
JWT_ALGORITHM = Config.JWT_ALGORITHM
JWT_EXPIRATION_DELTA = Config.JWT_EXPIRATION_DELTA

# Spectacular settings (API documentation)
SPECTACULAR_SETTINGS = {
    'TITLE': 'WelfareWatch API',
    'DESCRIPTION': '公司福利评价系统 API 文档',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
}

# Logging Configuration (企业级日志配置)
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[{levelname}] {asctime} {name} {module}.{funcName}:{lineno} - {message}',
            'style': '{',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
        'simple': {
            'format': '[{levelname}] {asctime} - {message}',
            'style': '{',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'console_debug': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'file_general': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': BASE_DIR / 'logs' / 'general.log',
            'maxBytes': 1024 * 1024 * 10,  # 10 MB
            'backupCount': 10,
            'formatter': 'verbose',
            'encoding': 'utf-8',
        },
        'file_error': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': BASE_DIR / 'logs' / 'error.log',
            'maxBytes': 1024 * 1024 * 10,  # 10 MB
            'backupCount': 10,
            'formatter': 'verbose',
            'encoding': 'utf-8',
        },
        'file_database': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': BASE_DIR / 'logs' / 'database.log',
            'maxBytes': 1024 * 1024 * 5,  # 5 MB
            'backupCount': 5,
            'formatter': 'verbose',
            'encoding': 'utf-8',
        },
        'file_security': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': BASE_DIR / 'logs' / 'security.log',
            'maxBytes': 1024 * 1024 * 10,  # 10 MB
            'backupCount': 10,
            'formatter': 'verbose',
            'encoding': 'utf-8',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        # Django 核心日志
        'django': {
            'handlers': ['console', 'file_general'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['file_error', 'mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.db.backends': {
            'handlers': ['file_database'],
            'level': 'WARNING' if DEBUG else 'ERROR',
            'propagate': False,
        },
        'django.security': {
            'handlers': ['file_security', 'mail_admins'],
            'level': 'INFO',
            'propagate': False,
        },
        # 应用日志
        'apps.accounts': {
            'handlers': ['console_debug', 'file_general', 'file_error'],
            'level': 'DEBUG' if DEBUG else 'INFO',
            'propagate': False,
        },
        'apps.companies': {
            'handlers': ['console_debug', 'file_general', 'file_error'],
            'level': 'DEBUG' if DEBUG else 'INFO',
            'propagate': False,
        },
        'apps.reviews': {
            'handlers': ['console_debug', 'file_general', 'file_error'],
            'level': 'DEBUG' if DEBUG else 'INFO',
            'propagate': False,
        },
        'apps.moderation': {
            'handlers': ['console_debug', 'file_general', 'file_error'],
            'level': 'DEBUG' if DEBUG else 'INFO',
            'propagate': False,
        },
        # 脚本日志
        'scripts': {
            'handlers': ['console', 'file_general'],
            'level': 'INFO',
            'propagate': False,
        },
    },
    'root': {
        'handlers': ['console', 'file_general', 'file_error'],
        'level': 'INFO',
    },
}

# 缓存配置
CACHES = {
    'default': {
        'BACKEND': Config.CACHE_BACKEND,
        'LOCATION': Config.CACHE_LOCATION,
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        },
        'KEY_PREFIX': 'welfarewatch',
        'TIMEOUT': 300,  # 5 minutes
    }
}

# 邮件配置
if Config.EMAIL_HOST_USER:
    EMAIL_BACKEND = Config.EMAIL_BACKEND
    EMAIL_HOST = Config.EMAIL_HOST
    EMAIL_PORT = Config.EMAIL_PORT
    EMAIL_USE_TLS = Config.EMAIL_USE_TLS
    EMAIL_HOST_USER = Config.EMAIL_HOST_USER
    EMAIL_HOST_PASSWORD = Config.EMAIL_HOST_PASSWORD
    DEFAULT_FROM_EMAIL = Config.EMAIL_HOST_USER
    
    # 管理员邮箱（接收错误报告）
    ADMINS = [(Config.ADMIN_NAME, Config.ADMIN_EMAIL)]
    MANAGERS = ADMINS
else:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

