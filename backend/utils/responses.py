"""
统一API响应格式
提供标准化的API响应结构
"""
from typing import Any, Optional, Dict
from rest_framework.response import Response
from rest_framework import status


class APIResponse:
    """
    统一的API响应类
    
    标准响应格式：
    {
        "code": 200,
        "message": "success",
        "data": {...},
        "timestamp": 1234567890
    }
    """
    
    @staticmethod
    def success(
        data: Any = None,
        message: str = "操作成功",
        code: int = status.HTTP_200_OK,
        **kwargs
    ) -> Response:
        """
        成功响应
        
        Args:
            data: 响应数据
            message: 响应消息
            code: HTTP状态码
            **kwargs: 其他参数
            
        Returns:
            Response: DRF Response对象
        """
        response_data = {
            "code": code,
            "message": message,
            "data": data,
        }
        response_data.update(kwargs)
        
        return Response(response_data, status=code)
    
    @staticmethod
    def error(
        message: str = "操作失败",
        code: int = status.HTTP_400_BAD_REQUEST,
        errors: Optional[Dict] = None,
        **kwargs
    ) -> Response:
        """
        错误响应
        
        Args:
            message: 错误消息
            code: HTTP状态码
            errors: 详细错误信息
            **kwargs: 其他参数
            
        Returns:
            Response: DRF Response对象
        """
        response_data = {
            "code": code,
            "message": message,
        }
        
        if errors:
            response_data["errors"] = errors
        
        response_data.update(kwargs)
        
        return Response(response_data, status=code)
    
    @staticmethod
    def created(
        data: Any = None,
        message: str = "创建成功",
        **kwargs
    ) -> Response:
        """创建成功响应"""
        return APIResponse.success(
            data=data,
            message=message,
            code=status.HTTP_201_CREATED,
            **kwargs
        )
    
    @staticmethod
    def no_content(message: str = "删除成功") -> Response:
        """无内容响应"""
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @staticmethod
    def unauthorized(message: str = "未授权访问") -> Response:
        """未授权响应"""
        return APIResponse.error(
            message=message,
            code=status.HTTP_401_UNAUTHORIZED
        )
    
    @staticmethod
    def forbidden(message: str = "没有权限") -> Response:
        """禁止访问响应"""
        return APIResponse.error(
            message=message,
            code=status.HTTP_403_FORBIDDEN
        )
    
    @staticmethod
    def not_found(message: str = "资源不存在") -> Response:
        """资源不存在响应"""
        return APIResponse.error(
            message=message,
            code=status.HTTP_404_NOT_FOUND
        )
    
    @staticmethod
    def validation_error(errors: Dict, message: str = "数据验证失败") -> Response:
        """验证错误响应"""
        return APIResponse.error(
            message=message,
            code=status.HTTP_400_BAD_REQUEST,
            errors=errors
        )
    
    @staticmethod
    def server_error(message: str = "服务器错误") -> Response:
        """服务器错误响应"""
        return APIResponse.error(
            message=message,
            code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


class PaginatedAPIResponse:
    """
    分页响应格式
    
    响应格式：
    {
        "code": 200,
        "message": "success",
        "data": {
            "count": 100,
            "next": "http://...",
            "previous": null,
            "results": [...]
        }
    }
    """
    
    @staticmethod
    def paginate(
        queryset,
        request,
        serializer_class,
        message: str = "获取成功"
    ) -> Response:
        """
        分页响应
        
        Args:
            queryset: 查询集
            request: 请求对象
            serializer_class: 序列化器类
            message: 响应消息
            
        Returns:
            Response: 分页响应
        """
        from rest_framework.pagination import PageNumberPagination
        
        paginator = PageNumberPagination()
        page = paginator.paginate_queryset(queryset, request)
        
        if page is not None:
            serializer = serializer_class(page, many=True)
            return Response({
                "code": status.HTTP_200_OK,
                "message": message,
                "data": {
                    "count": paginator.page.paginator.count,
                    "next": paginator.get_next_link(),
                    "previous": paginator.get_previous_link(),
                    "results": serializer.data
                }
            })
        
        serializer = serializer_class(queryset, many=True)
        return APIResponse.success(data=serializer.data, message=message)

