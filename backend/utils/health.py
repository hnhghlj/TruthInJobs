"""
健康检查端点
用于监控系统状态
"""
import logging
from django.http import JsonResponse
from django.views import View
from django.db import connection
from django.core.cache import cache
import time

logger = logging.getLogger('django')


class HealthCheckView(View):
    """
    健康检查端点
    GET /health/ - 返回系统健康状态
    """
    
    def get(self, request):
        """
        健康检查
        
        Returns:
            JsonResponse: 健康状态
        """
        health_status = {
            'status': 'healthy',
            'checks': {},
            'timestamp': time.time()
        }
        
        # 检查数据库连接
        db_healthy = self.check_database()
        health_status['checks']['database'] = {
            'status': 'healthy' if db_healthy else 'unhealthy',
            'message': 'Database connection OK' if db_healthy else 'Database connection failed'
        }
        
        # 检查缓存
        cache_healthy = self.check_cache()
        health_status['checks']['cache'] = {
            'status': 'healthy' if cache_healthy else 'unhealthy',
            'message': 'Cache working' if cache_healthy else 'Cache failed'
        }
        
        # 总体状态
        all_healthy = all(
            check['status'] == 'healthy' 
            for check in health_status['checks'].values()
        )
        health_status['status'] = 'healthy' if all_healthy else 'unhealthy'
        
        # 返回响应
        status_code = 200 if all_healthy else 503
        
        if not all_healthy:
            logger.error(f"Health check failed: {health_status}")
        
        return JsonResponse(health_status, status=status_code)
    
    def check_database(self) -> bool:
        """检查数据库连接"""
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                cursor.fetchone()
            return True
        except Exception as e:
            logger.error(f"Database health check failed: {e}")
            return False
    
    def check_cache(self) -> bool:
        """检查缓存"""
        try:
            test_key = 'health_check_test'
            test_value = 'ok'
            cache.set(test_key, test_value, 10)
            result = cache.get(test_key)
            return result == test_value
        except Exception as e:
            logger.error(f"Cache health check failed: {e}")
            return False


class ReadinessCheckView(View):
    """
    就绪检查端点
    GET /ready/ - 返回应用是否准备好接收流量
    """
    
    def get(self, request):
        """就绪检查"""
        # 检查数据库迁移是否完成
        try:
            from django.db.migrations.executor import MigrationExecutor
            executor = MigrationExecutor(connection)
            plan = executor.migration_plan(executor.loader.graph.leaf_nodes())
            
            if plan:
                return JsonResponse({
                    'status': 'not_ready',
                    'message': 'Pending migrations detected'
                }, status=503)
            
            return JsonResponse({
                'status': 'ready',
                'message': 'Application is ready'
            })
        except Exception as e:
            logger.error(f"Readiness check failed: {e}")
            return JsonResponse({
                'status': 'not_ready',
                'message': str(e)
            }, status=503)


class LivenessCheckView(View):
    """
    存活检查端点
    GET /alive/ - 返回应用是否存活
    """
    
    def get(self, request):
        """存活检查 - 简单返回200"""
        return JsonResponse({
            'status': 'alive',
            'message': 'Application is running'
        })

