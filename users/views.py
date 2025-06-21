from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

from .serializers import (
    UserAuthSerializer,
    UserRegisterSerializer,
    UserConfirmationSerializer,
)
from .models import UserConfirmationCode

# from django.core.mail import send_mail
# from django.conf import settings

@api_view(['POST'])
def registration_api_view(request):
    serializer = UserRegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    username = serializer.validated_data['username']
    password = serializer.validated_data['password']

    user = User.objects.create_user(
        username=username,
        password=password,
        is_active=False
    )

    code = UserConfirmationCode.objects.create(user=user)

    # Вариант с письмом (отключено):
    # from django.core.mail import send_mail
    # from django.conf import settings
    # try:
    #     send_mail(
    #         subject='Код подтверждения регистрации',
    #         message=f'Ваш код подтверждения: {code.code}',
    #         from_email=settings.DEFAULT_FROM_EMAIL,
    #         recipient_list=[user.email],  # если нужно вернуть email
    #         fail_silently=False,
    #     )
    # except Exception as e:
    #     print(f"Ошибка отправки письма: {e}")

    return Response(
        {
            "message": "Пользователь зарегистрирован. Введите код подтверждения.",
            "confirmation_code": code.code
        },
        status=status.HTTP_201_CREATED
    )


class ConfirmAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserConfirmationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data['username']
        code = serializer.validated_data['code']

        try:
            user = User.objects.get(username=username)
            if user.confirmation_code.code == code:
                user.is_active = True
                user.save()
                user.confirmation_code.delete()
                return Response({"message": "Пользователь подтвержден!"})
            return Response({"error": "Неверный код"}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"error": "Пользователь не найден"}, status=status.HTTP_404_NOT_FOUND)


class AuthAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserAuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(**serializer.validated_data)

        if user:
            if not user.is_active:
                return Response({"error": "Пользователь не подтвержден"}, status=status.HTTP_403_FORBIDDEN)

            token, _ = Token.objects.get_or_create(user=user)
            return Response({"token": token.key})

        return Response({"error": "Неверные учетные данные"}, status=status.HTTP_401_UNAUTHORIZED)
