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
from staff.models import ProcessAttendanceDaily,StaffLeaveTransaction
from student.models import Student,Guardian,StudentEnroll,ProcessStAttendanceDaily,StudentLeaveTransaction
from fees.models import FeesTransaction
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
        day_name = datetime.now().date().strftime('%A').lower()
        current_date = datetime.now().date()
        print(day_name)
        print(current_date)
        SITE_PROTOCOL = 'http://'
        if request.is_secure():
            SITE_PROTOCOL = 'https://'
        current_site = get_current_site(request).domain
        institution_id = self.request.user.institution
        branch_id = self.request.user.branch

        ''' For stuent user '''
        if Student.objects.filter(user=self.request.user.id,institution=institution_id, branch=branch_id).exists():
            user_info = Student.objects.get(user=self.request.user.id,institution=institution_id, branch=branch_id)
            dashboard_data['basic_info']['first_name'] = user_info.first_name
            dashboard_data['basic_info']['last_name'] = user_info.last_name
            dashboard_data['basic_info']['username'] = user_info.student_no
            if user_info.photo:
                dashboard_data['basic_info']['image'] = SITE_PROTOCOL+current_site + '/media/'+str(user_info.photo)
            else:
                dashboard_data['basic_info']['image'] = None
            # For Student Basic Information
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
            # For Current day Student Class Routiine
            dashboard_data['today_class_routine'] = []
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
            # For Teacher List
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
            # For Attendance List
            dashboard_data['attendance_list'] = []
            if ProcessStAttendanceDaily.objects.filter(student=user_info,status=True,is_active=True,institution=institution_id, branch=branch_id).exists():
                attn_lists = []
                for std_attn in ProcessStAttendanceDaily.objects.filter(student=user_info,status=True,is_active=True,institution=institution_id, branch=branch_id).order_by('-attn_date')[:30]:
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
            # For Student Leave Transaction
            dashboard_data['leave_app_list'] = []
            if StudentLeaveTransaction.objects.filter(apply_by=user_info,status=True,institution=institution_id, branch=branch_id).exists():
                leave_lists = []
                for leave_trns in StudentLeaveTransaction.objects.filter(apply_by=user_info,status=True,institution=institution_id, branch=branch_id).order_by('-start_date')[:30]:
                    leave_list = {}
                    leave_list['start_date'] = leave_trns.start_date
                    leave_list['end_date'] = leave_trns.end_date
                    leave_list['duration'] = leave_trns.day_count
                    leave_list['reason'] = leave_trns.reason_for_leave
                    if leave_trns.app_status:
                        leave_list['status'] = leave_trns.app_status.title
                    else:
                        leave_list['status'] = None
                    leave_lists.append(leave_list)
                dashboard_data['leave_app_list'] = leave_lists
        elif Guardian.objects.filter(user=self.request.user.id).exists():
            user_info = Guardian.objects.get(user=self.request.user.id)
            dashboard_data['basic_info']['first_name'] = user_info.first_name
            dashboard_data['basic_info']['last_name'] = user_info.last_name
            dashboard_data['basic_info']['username'] = user_info.guardian_no
            # dashboard_data['basic_info']['nid'] = user_info.nid
            dashboard_data['basic_info']['role'] = 'Guardian'
            if user_info.photo:
                dashboard_data['basic_info']['image'] = SITE_PROTOCOL+current_site + '/media/'+str(user_info.photo)
            else:
                dashboard_data['basic_info']['image'] = None
            dashboard_data['student_info'] = []
            std_lists = []
            for std_info in Guardian.objects.filter(status=True,nid=user_info.nid):
                std_list = {}
                student_pk = std_info.student.id
                std_list['id'] = student_pk
                std_list['first_name'] = std_info.student.first_name
                std_list['last_name'] = std_info.student.last_name
                std_list['username'] = std_info.student.student_no
                if std_info.student.photo:
                    std_list['image'] = SITE_PROTOCOL+current_site + '/media/'+str(std_info.student.photo)
                else:
                    std_list['image'] = None
                std_list['basic_info'] = {}
                # For Student Basic Information
                if StudentEnroll.objects.filter(student=std_info.student,status=True,is_active=True,institution=std_info.student.institution, branch=std_info.student.branch).exists():
                    std_enroll = StudentEnroll.objects.filter(student=std_info.student,status=True,is_active=True,institution=std_info.student.institution, branch=std_info.student.branch).order_by('-id').last()
                    session_name = std_enroll.session.session
                    version_name = std_enroll.version.version
                    class_name = std_enroll.class_name.name
                    section = std_enroll.section.section
                    roll_no = std_enroll.roll
                    std_list['basic_info']['session'] = session_name
                    std_list['basic_info']['version'] = version_name
                    std_list['basic_info']['class_name'] = class_name
                    std_list['basic_info']['section'] = section
                    std_list['basic_info']['roll'] = roll_no
                    # For Current day Student Class Routiine
                    std_list['today_class_routine'] = []
                    day_name = datetime.now().date().strftime('%A').lower()
                    day_id = Days.objects.filter(status=True,long_name__iexact=day_name,institution=std_info.student.institution, branch=std_info.student.branch).last()
                    routine_mst = ClassRoutineMst.objects.filter(session=std_enroll.session,version=std_enroll.version,class_name=std_enroll.class_name,section=std_enroll.section,status=True,institution=std_info.student.institution, branch=std_info.student.branch).last()
                    class_routines = []
                    for routine_dtl in ClassRoutiineDtl.objects.filter(class_routine_mst=routine_mst,status=True,institution=std_info.student.institution, branch=std_info.student.branch,day=day_id):
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
                    std_list['today_class_routine'] = class_routines
                    # For Teacher List
                    std_list['teacher_list'] = []
                    teacher_lists = []
                    class_teacher = ClassTeacher.objects.filter(status=True,institution=std_info.student.institution, branch=std_info.student.branch,session=std_enroll.session,version=std_enroll.version,class_name=std_enroll.class_name,section=std_enroll.section).last()
                    for teacher in ClassRoutiineDtl.objects.filter(class_routine_mst=routine_mst,status=True,institution=std_info.student.institution, branch=std_info.student.branch):
                        teacher_info = {}
                        if class_teacher and class_teacher.teacher.id == teacher.teacher.id:
                            teacher_info['class_teacher'] = True
                        else:
                            teacher_info['class_teacher'] = False
                        teacher_info['name'] = teacher.teacher.first_name +' '+teacher.teacher.last_name
                        teacher_info['subject'] = teacher.subject.code +' - '+teacher.subject.name
                        teacher_info['phone'] = teacher.teacher.mobile_no
                        teacher_lists.append(teacher_info)
                    std_list['teacher_list'] = teacher_lists
                    # For Attendance List
                    std_list['attendance_list'] = []
                    if ProcessStAttendanceDaily.objects.filter(student=std_info.student,status=True,is_active=True,institution=std_info.student.institution, branch=std_info.student.branch).exists():
                        attn_lists = []
                        for std_attn in ProcessStAttendanceDaily.objects.filter(student=std_info.student,status=True,is_active=True,institution=std_info.student.institution, branch=std_info.student.branch).order_by('-attn_date')[:30]:
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
                        std_list['attendance_list'] = attn_lists
                    # For Student Leave Transaction
                    std_list['leave_app_list'] = []
                    if StudentLeaveTransaction.objects.filter(apply_by=std_info.student,status=True,institution=std_info.student.institution, branch=std_info.student.branch).exists():
                        leave_lists = []
                        for leave_trns in StudentLeaveTransaction.objects.filter(apply_by=std_info.student,status=True,institution=std_info.student.institution, branch=std_info.student.branch).order_by('-start_date')[:30]:
                            leave_list = {}
                            leave_list['start_date'] = leave_trns.start_date
                            leave_list['end_date'] = leave_trns.end_date
                            leave_list['duration'] = leave_trns.day_count
                            leave_list['reason'] = leave_trns.reason_for_leave
                            if leave_trns.app_status:
                                leave_list['status'] = leave_trns.app_status.title
                            else:
                                leave_list['status'] = None
                            leave_lists.append(leave_list)
                        std_list['leave_app_list'] = leave_lists
                    # For Student Fees Information
                    std_list['fees_trns'] = []
                    if FeesTransaction.objects.filter(student=std_info.student,status=True,institution=std_info.student.institution, branch=std_info.student.branch).exists():
                        fees_lists = []
                        for fee_trns in FeesTransaction.objects.filter(student=std_info.student,status=True,institution=std_info.student.institution, branch=std_info.student.branch)[:12]:
                            fees_list = {}
                            fees_list['due_date'] = fee_trns.fees_detail.due_date
                            fees_list['fees_type'] = fee_trns.fees_detail.fees_type.name
                            fees_list['amount'] = fee_trns.fees_detail.amount
                            fees_list['status'] = fee_trns.pay_status
                            fees_lists.append(fees_list)
                        std_list['fees_trns'] = fees_lists
                std_lists.append(std_list)
            dashboard_data['student_info'] = std_lists
        elif Staff.objects.filter(user=self.request.user.id,institution=institution_id, branch=branch_id,status=True).exists():
            user_info = Staff.objects.get(user=self.request.user.id,status=True)
            dashboard_data['basic_info']['first_name'] = user_info.first_name
            dashboard_data['basic_info']['last_name'] = user_info.last_name
            dashboard_data['basic_info']['username'] = user_info.staff_id
            # dashboard_data['basic_info']['nid'] = user_info.nid
            dashboard_data['basic_info']['role'] = user_info.role.name
            dashboard_data['basic_info']['shift'] = user_info.shift.name
            if user_info.photo:
                dashboard_data['basic_info']['image'] = SITE_PROTOCOL+current_site + '/media/'+str(user_info.photo)
            else:
                dashboard_data['basic_info']['image'] = None
            dashboard_data['basic_info']['total_student'] = 0
            dashboard_data['basic_info']['total_present'] = 0
            dashboard_data['basic_info']['total_absent'] = 0
            if ClassTeacher.objects.filter(status=True,institution=institution_id, branch=branch_id,teacher=user_info).exists():
                class_info = ClassTeacher.objects.filter(status=True,institution=institution_id, branch=branch_id,teacher=user_info).last()
                student_count = StudentEnroll.objects.filter(student__shift=user_info.shift,is_active=True,status=True,session=class_info.session,version=class_info.version,class_name=class_info.class_name,section=class_info.section).count()
                dashboard_data['basic_info']['total_student'] = student_count
                std_ids = []
                if student_count > 0:
                    for student_info in StudentEnroll.objects.filter(student__shift=user_info.shift,is_active=True,status=True,session=class_info.session,version=class_info.version,class_name=class_info.class_name,section=class_info.section):
                        std_ids.append(student_info.student.id)
                    total_present = ProcessStAttendanceDaily.objects.filter(shift=user_info.shift,attn_type__name__in=['Present', 'Late'],status=True,is_active=True,student__in=std_ids,attn_date=current_date).count()
                    total_absent = ProcessStAttendanceDaily.objects.filter(shift=user_info.shift,attn_type__name__in=['Absent'],status=True,is_active=True,student__in=std_ids,attn_date=current_date).count()
                    dashboard_data['basic_info']['total_present'] = total_present
                    dashboard_data['basic_info']['total_absent'] = total_absent
            day_id = Days.objects.filter(status=True,long_name__iexact=day_name,institution=institution_id, branch=branch_id).last()
            dashboard_data['today_class_routine'] = []
            class_routines = []
            for routine_dtl in ClassRoutiineDtl.objects.filter(teacher=user_info,status=True,institution=institution_id, branch=branch_id,day=day_id).order_by('class_period__start_time'):
                class_routine = {}
                class_routine['start_time'] = routine_dtl.class_period.start_time
                class_routine['end_time'] = routine_dtl.class_period.end_time
                class_routine['subject'] = routine_dtl.subject.name
                class_routine['class_name'] = routine_dtl.class_routine_mst.class_name.name
                class_routine['section'] = routine_dtl.class_routine_mst.section.section
                class_routine['version'] = routine_dtl.class_routine_mst.version.version
                if routine_dtl.class_routine_mst.group:
                    class_routine['group'] = routine_dtl.class_routine_mst.group.name
                else:
                    class_routine['group'] = None
                class_routine['room_no'] = routine_dtl.class_room.room_no
                class_routine['buildingg'] = routine_dtl.class_room.building
                cls_present = ProcessStAttendanceDaily.objects.filter(session=routine_dtl.class_routine_mst.session,version=routine_dtl.class_routine_mst.version,class_name=routine_dtl.class_routine_mst.class_name,section=routine_dtl.class_routine_mst.section,attn_type__name__in=['Present', 'Late'],status=True,is_active=True,attn_date=current_date).count()
                cls_absent = ProcessStAttendanceDaily.objects.filter(session=routine_dtl.class_routine_mst.session,version=routine_dtl.class_routine_mst.version,class_name=routine_dtl.class_routine_mst.class_name,section=routine_dtl.class_routine_mst.section,attn_type__name__in=['Absent'],status=True,is_active=True,attn_date=current_date).count()
                class_routine['present'] = cls_present
                class_routine['absent'] = cls_absent
                class_routines.append(class_routine)
            dashboard_data['today_class_routine'] = class_routines
            # For Attendance List
            dashboard_data['attendance_list'] = []
            if ProcessAttendanceDaily.objects.filter(staff=user_info,status=True,is_active=True,institution=institution_id, branch=branch_id).exists():
                attn_lists = []
                for std_attn in ProcessAttendanceDaily.objects.filter(staff=user_info,status=True,is_active=True,institution=institution_id, branch=branch_id).order_by('-attn_date')[:30]:
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
            # For Student Leave Transaction
            dashboard_data['leave_app_list'] = []
            if StaffLeaveTransaction.objects.filter(apply_by=user_info,status=True,institution=institution_id, branch=branch_id).exists():
                leave_lists = []
                for leave_trns in StaffLeaveTransaction.objects.filter(apply_by=user_info,status=True,institution=institution_id, branch=branch_id).order_by('-start_date')[:30]:
                    leave_list = {}
                    leave_list['start_date'] = leave_trns.start_date
                    leave_list['end_date'] = leave_trns.end_date
                    leave_list['duration'] = leave_trns.day_count
                    leave_list['leave_type'] = leave_trns.leave_type.name
                    leave_list['reason'] = leave_trns.reason_for_leave
                    if leave_trns.app_status:
                        leave_list['status'] = leave_trns.app_status.title
                    else:
                        leave_list['status'] = None
                    leave_lists.append(leave_list)
                dashboard_data['leave_app_list'] = leave_lists        
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