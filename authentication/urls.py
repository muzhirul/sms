from django.urls import path,include
from .views import UserLoginView,UserV2LoginView,UserV3LoginView
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView, TokenVerifyView

urlpatterns = [
    path('api/token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/login', UserLoginView.as_view(), name='login'),
    path('api/v2/login', UserV2LoginView.as_view(), name='loginv2'),
    path('api/v3/login', UserV3LoginView.as_view(), name='loginv3'),
    path('api/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify', TokenVerifyView.as_view(), name='token_verify'),
]