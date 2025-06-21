from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError


# 🔹 Базовый сериализатор с username и password
class UserBaseSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True)


# 🔹 Авторизация — просто базовый сериализатор
class UserAuthSerializer(UserBaseSerializer):
    pass


# 🔹 Регистрация — проверяет, что пользователь уникальный
class UserRegisterSerializer(UserBaseSerializer):
    def validate_username(self, username):
        if User.objects.filter(username=username).exists():
            raise ValidationError('Пользователь с таким именем уже существует.')
        return username


# 🔹 Подтверждение — принимает username и 6-значный код
class UserConfirmationSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    code = serializers.CharField(max_length=6)
