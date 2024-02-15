from django.urls import path
from .views import UserRegistrationView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'), #ендпоинт регистрации нового пользователя
    path('token/', TokenObtainPairView.as_view(),name='token_obtain_pair'),  #ендпоинт генерации access/refresh токенов
    path('token/refresh', TokenRefreshView.as_view(),name='token_refresh'), #ендпоинт refresh токена
]
