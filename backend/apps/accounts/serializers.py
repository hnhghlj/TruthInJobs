from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User
from .authentication import generate_jwt_token


class UserSerializer(serializers.ModelSerializer):
    """用户序列化器"""
    
    class Meta:
        model = User
        fields = (
            'id', 'username', 'email', 'phone', 'user_type', 
            'avatar', 'bio', 'anonymous_name',
            'review_count', 'comment_count',
            'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'user_type', 'review_count', 'comment_count', 'created_at', 'updated_at')


class UserRegisterSerializer(serializers.ModelSerializer):
    """用户注册序列化器"""
    password = serializers.CharField(write_only=True, min_length=6)
    password_confirm = serializers.CharField(write_only=True, min_length=6)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password_confirm', 'phone')
    
    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("两次密码不一致")
        return data
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        
        user = User(**validated_data)
        user.set_password(password)
        
        # 生成匿名昵称
        if not user.anonymous_name:
            user.anonymous_name = f"匿名用户{user.username[:4]}"
        
        user.save()
        return user


class UserLoginSerializer(serializers.Serializer):
    """用户登录序列化器"""
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise serializers.ValidationError("用户名或密码错误")
            if not user.is_active:
                raise serializers.ValidationError("用户已被禁用")
            data['user'] = user
        else:
            raise serializers.ValidationError("必须提供用户名和密码")
        
        return data
    
    def create(self, validated_data):
        user = validated_data['user']
        token = generate_jwt_token(user)
        return {
            'token': token,
            'user': UserSerializer(user).data
        }


class ChangePasswordSerializer(serializers.Serializer):
    """修改密码序列化器"""
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, min_length=6)
    new_password_confirm = serializers.CharField(write_only=True, min_length=6)
    
    def validate(self, data):
        if data['new_password'] != data['new_password_confirm']:
            raise serializers.ValidationError("两次新密码不一致")
        return data
    
    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("原密码错误")
        return value
    
    def save(self):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user

