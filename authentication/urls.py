from django.urls import path,include
from .views import UserLoginView
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView, TokenVerifyView

urlpatterns = [
    path('api/token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/login', UserLoginView.as_view(), name='login'),
    path('api/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify', TokenVerifyView.as_view(), name='token_verify'),
]