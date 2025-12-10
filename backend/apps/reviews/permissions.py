from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    对象级权限：只允许对象的所有者编辑
    """
    
    def has_object_permission(self, request, view, obj):
        # 读取权限允许任何请求
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # 写权限只允许所有者
        return obj.user == request.user


class IsModerator(permissions.BasePermission):
    """
    只允许审核员和管理员访问
    """
    
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_moderator()

