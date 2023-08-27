from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import LoginSerializer
from django.contrib.auth import authenticate
# Create your views here.
class UserLoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password']
        )
        if user is None:
            return Response({
                'code':401,
                'message': 'Invalid credentials',
                'error':[],
                'data': None
                }, status=status.HTTP_401_UNAUTHORIZED)
        refresh = RefreshToken.for_user(user)
        return Response({
            'code':200,
            'message':'Success',
            'error':[],
            'data':{
                'user': LoginSerializer(user).data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        },status=status.HTTP_200_OK)