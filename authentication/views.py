from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import LoginSerializer, LoginSerializer2, LoginSerializer3,LoginSerializer4
from django.contrib.auth import authenticate
from academic.models import *
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from setup_app.models import Role,Permission,Menu
from django.db.models import Q
from django.contrib.sites.shortcuts import get_current_site


class UserV4LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer4(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password']
        )
        SITE_PROTOCOL = 'http://'
        if request.is_secure():
            SITE_PROTOCOL = 'https://'
        current_site = get_current_site(request).domain
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
        user_serializer = LoginSerializer4(user)
        user_data = user_serializer.data
        menu_info = {}
        role_id = []
        user_data['menus'] = []
        for role in user.role.all():
            role_id.append((role.id))
            # for parent in Permission.objects.filter(Q(can_create=True) | Q(can_view=True) | Q(can_update=True) | Q(can_delete=True), role=role).values_list('menu__parent', flat=True).distinct():
            #     parent_name = Menu.objects.get(id=parent,parent_id__isnull=True)
                # app_name = parent_name.name
                # if app_name not in menu_info:
                #     menu_info[app_name] = {}
                # for child in Permission.objects.filter(Q(can_create=True) | Q(can_view=True) | Q(can_update=True) | Q(can_delete=True), role=role, menu__parent= parent).distinct():
                #     model_name = child.menu.name
                #     menu_info[app_name][model_name] = []
        parent_id = []
        for parent in Permission.objects.filter(Q(can_create=True) | Q(can_view=True) | Q(can_update=True) | Q(can_delete=True), role__in=role_id,status=True).values_list('menu__parent', flat=True).distinct():
            if parent:
                parent_id.append(parent)
        main_menus = []
        print(parent_id)
        parent_menus = Menu.objects.filter(id__in=parent_id,parent_id__isnull=True,status=True).order_by('sl_no')
        for parent_menu in parent_menus:
            # print(parent_menu.name)
            main_menu = {}
            main_menu['id'] = parent_menu.id
            main_menu['name'] = parent_menu.name
            if parent_menu.icon:
                main_menu['icon'] = SITE_PROTOCOL+current_site + '/media/'+str(parent_menu.icon)
            else:
                main_menu['icon'] = ''
            main_menu['order'] = parent_menu.sl_no
            child_id = []
            permissions = Permission.objects.filter(Q(can_create=True) | Q(can_view=True) | Q(can_update=True) | Q(can_delete=True), role__in=role_id,menu__parent= parent_menu.id,status=True).values_list('menu__id', flat=True).distinct()
            for permission in permissions:
                child_id.append(permission)
            child_menus = Menu.objects.filter(id__in=child_id,parent_id__isnull=False,status=True).order_by('sl_no')
            main_menu['sub_menu'] = []
            menu_child = []
            
            for child_menu in child_menus:
                sub_memu = {}
                sub_memu['id'] = child_menu.id
                sub_memu['name'] = child_menu.name
                if child_menu.slug:
                    sub_memu['slug'] = '/'+parent_menu.slug+'/'+child_menu.slug
                sub_memu['order'] = child_menu.sl_no
                sub_memu['permission'] = []
                userPermission = []
                user_permissions = Permission.objects.filter(Q(can_create=True) | Q(can_view=True) | Q(can_update=True) | Q(can_delete=True),menu= child_menu.id,status=True)
                for user_permission in user_permissions:
                    if user_permission.can_create:
                        userPermission.append('create')
                    if user_permission.can_view:
                        userPermission.append('view')
                    if user_permission.can_update:
                        userPermission.append('update')
                    if user_permission.can_delete:
                        userPermission.append('delete')
                userPermission = set(userPermission)
                sub_memu['permission'] = userPermission
                menu_child.append(sub_memu)
            main_menu['sub_menu'] = menu_child
            main_menus.append(main_menu)
        user_data['menus'] = main_menus        
        user_data['token'] = {}
        user_data['token']['refresh'] = str(refresh)
        user_data['token']['access'] = str(refresh.access_token)
        
        return Response({
            'code':200,
            'message':'Success',
            'error':[],
            'data':user_data},status=status.HTTP_200_OK)


class UserV3LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer3(data=request.data)
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
        user_serializer = LoginSerializer3(user)
        user_data = user_serializer.data
        menu_info = {}
        for role in user.role.all():
            for parent in Permission.objects.filter(Q(can_create=True) | Q(can_view=True) | Q(can_update=True) | Q(can_delete=True), role=role).values_list('menu__parent', flat=True).distinct():
                parent_name = Menu.objects.get(id=parent,parent_id__isnull=True)
                app_name = parent_name.name
                if app_name not in menu_info:
                    menu_info[app_name] = {}
                for child in Permission.objects.filter(Q(can_create=True) | Q(can_view=True) | Q(can_update=True) | Q(can_delete=True), role=role, menu__parent= parent).distinct():
                    model_name = child.menu.name
                    menu_info[app_name][model_name] = []
        user_data['menus'] = menu_info        
        user_data['token'] = {}
        user_data['token']['refresh'] = str(refresh)
        user_data['token']['access'] = str(refresh.access_token)
        
        return Response({
            'code':200,
            'message':'Success',
            'error':[],
            'data':user_data},status=status.HTTP_200_OK)

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