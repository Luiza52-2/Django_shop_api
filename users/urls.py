from django.urls import path
from .views import registration_api_view, ConfirmAPIView, AuthAPIView

urlpatterns = [
    path('registration/', registration_api_view, name='user-registration'),
    path('confirm/', ConfirmAPIView.as_view(), name='user-confirmation'),
    path('auth/', AuthAPIView.as_view(), name='user-auth'),
]
