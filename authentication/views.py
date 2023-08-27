from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import LoginSerializer
from django.contrib.auth import authenticate
from django.contrib.auth.models import Permission
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
        user_serializer = LoginSerializer(user)
        user_data = user_serializer.data
        """
        # Include detailed permission data for each group
        group_data = []
        for group in user.groups.all():
            group_permissions = Permission.objects.filter(group=group)
            group_data.append({
                'name': group.name,
                'permissions': [
                    {
                        'id': permission.id,
                        'name': permission.name,
                        'codename': permission.codename,
                    }
                    for permission in group_permissions
                ]
            })

        user_data['groups'] = group_data
        """
        user_data['token'] = {}
        user_data['token']['refresh'] = str(refresh)
        user_data['token']['access'] = str(refresh.access_token)
        return Response({
            'code':200,
            'message':'Success',
            'error':[],
            'data':user_data},status=status.HTTP_200_OK)