from django.urls import path
from . import views

urlpatterns = [
    path('registration/', views.registration_api_view, name='user-registration'),
    path('confirm/', views.confirm_api_view, name='user-confirmation'),
    path('auth/', views.auth_api_view, name='user-auth'),
]
