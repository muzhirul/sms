from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, permissions
from sms.utils import CustomResponse
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import LoginSerializer, LoginSerializer2, LoginSerializer3,LoginSerializer4
from django.contrib.auth import authenticate
from academic.models import *
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from setup_app.models import Role,Permission,Menu
from student.models import Student,Guardian,StudentEnroll,ProcessStAttendanceDaily
from django.db.models import Q
from django.contrib.sites.shortcuts import get_current_site
from datetime import datetime


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
        user_data['user'] = {}
        
        if Student.objects.filter(user=user_data['id']).exists():
            user_info = Student.objects.get(user=user_data['id'])
            user_data['user']['first_name'] = user_info.first_name
            user_data['user']['last_name'] = user_info.last_name
            user_data['user']['username'] = user_info.student_no
            if user_info.photo:
                user_data['user']['image'] = SITE_PROTOCOL+current_site + '/media/'+str(user_info.photo)
            else:
                user_data['user']['image'] = None
            user_data['user']['role'] = 'Student'

        elif Staff.objects.filter(user=user_data['id']).exists():
            user_info = Staff.objects.get(user=user_data['id'])
            user_data['user']['first_name'] = user_info.first_name
            user_data['user']['last_name'] = user_info.last_name
            user_data['user']['username'] = user_info.staff_id
            if user_info.photo:
                user_data['user']['image'] = SITE_PROTOCOL+current_site + '/media/'+str(user_info.photo)
            else:
                user_data['user']['image'] = None
            user_data['user']['role'] = user_info.role.name

        elif Guardian.objects.filter(user=user_data['id']).exists():
            user_info = Guardian.objects.get(user=user_data['id'])
            user_data['user']['first_name'] = user_info.first_name
            user_data['user']['last_name'] = user_info.last_name
            user_data['user']['username'] = user_info.guardian_no
            if user_info.photo:
                user_data['user']['image'] = SITE_PROTOCOL+current_site + '/media/'+str(user_info.photo)
            else:
                user_data['user']['image'] = None
            user_data['user']['role'] = 'Guardian'
        
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
            main_menu['icon_text'] = parent_menu.icon_text
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
                user_permissions = Permission.objects.filter(Q(can_create=True) | Q(can_view=True) | Q(can_update=True) | Q(can_delete=True), role__in=role_id,menu= child_menu.id,status=True)
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

class DashboardView(generics.ListAPIView):
    # Requires a valid JWT token for access
    permission_classes = [permissions.IsAuthenticated]
    def list(self, request, *args, **kwargs):
        dashboard_data = {}
        dashboard_data['basic_info'] = {}
        SITE_PROTOCOL = 'http://'
        if request.is_secure():
            SITE_PROTOCOL = 'https://'
        current_site = get_current_site(request).domain
        institution_id = self.request.user.institution
        branch_id = self.request.user.branch
        if Student.objects.filter(user=self.request.user.id,institution=institution_id, branch=branch_id).exists():
            user_info = Student.objects.get(user=self.request.user.id,institution=institution_id, branch=branch_id)
            dashboard_data['basic_info']['first_name'] = user_info.first_name
            dashboard_data['basic_info']['last_name'] = user_info.last_name
            dashboard_data['basic_info']['username'] = user_info.student_no
            if user_info.photo:
                dashboard_data['basic_info']['image'] = SITE_PROTOCOL+current_site + '/media/'+str(user_info.photo)
            else:
                dashboard_data['basic_info']['image'] = None
            if StudentEnroll.objects.filter(student=user_info,status=True,is_active=True,institution=institution_id, branch=branch_id).exists():
                std_enroll = StudentEnroll.objects.filter(student=user_info,status=True,is_active=True,institution=institution_id, branch=branch_id).order_by('-id').last()
                session_name = std_enroll.session.session
                version_name = std_enroll.version.version
                class_name = std_enroll.class_name.name
                section = std_enroll.section.section
                roll_no = std_enroll.roll
                dashboard_data['basic_info']['session'] = session_name
                dashboard_data['basic_info']['version'] = version_name
                dashboard_data['basic_info']['class_name'] = class_name
                dashboard_data['basic_info']['section'] = section
                dashboard_data['basic_info']['roll'] = roll_no
            dashboard_data['basic_info']['role'] = 'Student'
        
            dashboard_data['today_class_routine'] = []
            day_name = datetime.now().date().strftime('%A').lower()
            day_id = Days.objects.filter(status=True,long_name__iexact=day_name,institution=institution_id, branch=branch_id).last()
            routine_mst = ClassRoutineMst.objects.filter(session=std_enroll.session,version=std_enroll.version,class_name=std_enroll.class_name,section=std_enroll.section,status=True,institution=institution_id, branch=branch_id).last()
            class_routines = []
            for routine_dtl in ClassRoutiineDtl.objects.filter(class_routine_mst=routine_mst,status=True,institution=institution_id, branch=branch_id,day=day_id):
                class_routine = {}
                class_routine['subject'] = routine_dtl.subject.name
                class_routine['room_no'] = routine_dtl.class_room.room_no
                class_routine['building_name'] = routine_dtl.class_room.building
                class_routine['floor'] = routine_dtl.class_room.floor_type.name
                class_routine['start_time'] = routine_dtl.class_period.start_time
                class_routine['end_time'] = routine_dtl.class_period.end_time
                class_routine['teacher'] = routine_dtl.teacher.first_name +' '+routine_dtl.teacher.last_name
                # class_routine['time_slot'] = f"{str(routine_dtl.class_period.start_time) +'-'+str(routine_dtl.class_period.end_time)}"
                class_routines.append(class_routine)
            dashboard_data['today_class_routine'] = class_routines
            dashboard_data['teacher_list'] = []
            teacher_lists = []
            class_teacher = ClassTeacher.objects.filter(status=True,institution=institution_id, branch=branch_id,session=std_enroll.session,version=std_enroll.version,class_name=std_enroll.class_name,section=std_enroll.section).last()
            for teacher in ClassRoutiineDtl.objects.filter(class_routine_mst=routine_mst,status=True,institution=institution_id, branch=branch_id):
                teacher_info = {}
                if class_teacher.teacher.id == teacher.teacher.id:
                    teacher_info['class_teacher'] = True
                else:
                    teacher_info['class_teacher'] = False
                teacher_info['name'] = teacher.teacher.first_name +' '+teacher.teacher.last_name
                teacher_info['subject'] = teacher.subject.code +' - '+teacher.subject.name
                teacher_info['phone'] = teacher.teacher.mobile_no
                teacher_lists.append(teacher_info)
            dashboard_data['teacher_list'] = teacher_lists
            if ProcessStAttendanceDaily.objects.filter(student=user_info,status=True,is_active=True,institution=institution_id, branch=branch_id).exists():
                dashboard_data['attendance_list'] = []
                attn_lists = []
                for std_attn in ProcessStAttendanceDaily.objects.filter(student=user_info,status=True,is_active=True,institution=institution_id, branch=branch_id).order_by('-attn_date'):
                    attn_list = {}
                    if std_attn.in_time:
                        in_time = (std_attn.in_time.time())
                    else:
                        in_time = None
                    if std_attn.out_time:
                        out_time = (std_attn.out_time.time())
                    else:
                        out_time = None
                    attn_list['date'] = std_attn.attn_date
                    attn_list['shift'] = std_attn.shift.name
                    attn_list['in_time'] = in_time
                    attn_list['out_time'] = out_time
                    attn_list['status'] = std_attn.attn_type.name
                    attn_lists.append(attn_list)
                dashboard_data['attendance_list'] = attn_lists

        
        return Response({
            'code':200,
            'message':'Success',
            'error':[],
            'data':dashboard_data},status=status.HTTP_200_OK)

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