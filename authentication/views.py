from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import LoginSerializer, LoginSerializer2
from django.contrib.auth import authenticate
from academic.models import *
from django.contrib.auth.models import Permission
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType


class UserV2LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer2(data=request.data)
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
        # if not user.is_active:
        #     raise forms.ValidationError('Account disabled, contact admin')
        if not user.is_verified:
            return Response({
                'code':401,
                'message': 'Account is not verfied',
                'error':[],
                'data': None
                }, status=status.HTTP_401_UNAUTHORIZED)
        
        refresh = RefreshToken.for_user(user)
        user_serializer = LoginSerializer2(user)
        user_data = user_serializer.data
        
        permission_info = {}
        for group in user.groups.all():
            for content_type_id  in Permission.objects.filter(group=group).values_list('content_type_id', flat=True).distinct():
                content_type = ContentType.objects.get(id=content_type_id)
                app_label = content_type.app_label
                model_name = content_type.model
                if app_label not in permission_info:
                    permission_info[app_label] = {}
                permissions = Permission.objects.filter(content_type=content_type,group=group)
                permission_names = [permission.codename for permission in permissions]
                permission_info[app_label][model_name] = permission_names
        user_data['menus'] = permission_info
        user_data['token'] = {}
        user_data['token']['refresh'] = str(refresh)
        user_data['token']['access'] = str(refresh.access_token)
        return Response({
            'code':200,
            'message':'Success',
            'error':[],
            'data':user_data},status=status.HTTP_200_OK)

# Create your views here.
class UserLoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password']
        )
        # if not user:
        #     raise forms.ValidationError('Invalid Credentials')
        # content_type = ContentType.objects.all()
        # print(content_type)
        if user is None:
            return Response({
                'code':401,
                'message': 'Invalid credentials',
                'error':[],
                'data': None
                }, status=status.HTTP_401_UNAUTHORIZED)
        # if not user.is_active:
        #     raise forms.ValidationError('Account disabled, contact admin')
        if not user.is_verified:
            return Response({
                'code':401,
                'message': 'Account is not verfied',
                'error':[],
                'data': None
                }, status=status.HTTP_401_UNAUTHORIZED)
        
        refresh = RefreshToken.for_user(user)
        user_serializer = LoginSerializer(user)
        user_data = user_serializer.data
        
        """
        group_data = []
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