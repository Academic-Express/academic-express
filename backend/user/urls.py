from django.urls import path
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView, TokenVerifyView)

from . import views

app_name = 'user'
urlpatterns = [
    path('register', views.register, name='register'),
    path('login', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('login/verify', TokenVerifyView.as_view(), name='token_verify'),
    path('profile', views.UserView.as_view(), name='get_current_user'),
    path('profile/<int:pk>', views.get_user_by_id, name='get_user_by_id'),
    path('change-password', views.change_password, name='change_password'),
]
