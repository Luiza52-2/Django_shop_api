from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

from .serializers import (
    UserAuthSerializer,
    UserRegisterSerializer,
    UserConfirmationSerializer,
)
from .models import UserConfirmationCode


@api_view(['POST'])
def registration_api_view(request):
    serializer = UserRegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    username = serializer.validated_data['username']
    password = serializer.validated_data['password']

    user = User.objects.create_user(username=username, password=password, is_active=False)

    # Генерируем код подтверждения
    code = UserConfirmationCode.objects.create(user=user)

    return Response(
        {
            "message": "Пользователь зарегистрирован. Введите код подтверждения.",
            "user_id": user.id,
            "confirmation_code": code.code  # ⚠️ Только для отладки. В реальности отправлять по email
        },
        status=status.HTTP_201_CREATED
    )


@api_view(['POST'])
def confirm_api_view(request):
    serializer = UserConfirmationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    username = serializer.validated_data['username']
    code = serializer.validated_data['code']

    try:
        user = User.objects.get(username=username)
        if user.confirmation_code.code == code:
            user.is_active = True
            user.save()
            user.confirmation_code.delete()  # удалим код после подтверждения
            return Response({"message": "Пользователь подтвержден!"})
        return Response({"error": "Неверный код"}, status=status.HTTP_400_BAD_REQUEST)
    except User.DoesNotExist:
        return Response({"error": "Пользователь не найден"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def auth_api_view(request):
    serializer = UserAuthSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    user = authenticate(**serializer.validated_data)

    if user:
        if not user.is_active:
            return Response({"error": "Пользователь не подтвержден"}, status=status.HTTP_403_FORBIDDEN)

        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token": token.key})

    return Response({"error": "Неверные учетные данные"}, status=status.HTTP_401_UNAUTHORIZED)
