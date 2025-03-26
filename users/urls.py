from django.urls import path
from .views import (
    CustomTokenObtainPairView,
    CustomTokenRefreshView, 
    CustomTokenVerifyView,
    LogoutView,
    UpdtaeUserView
)

urlpatterns = [
    path('jwt/create/', CustomTokenObtainPairView.as_view()),
    path('jwt/refresh/', CustomTokenRefreshView.as_view()),
    path('jwt/verify/', CustomTokenVerifyView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('update-user/', UpdtaeUserView.as_view(), name='update-user')
]