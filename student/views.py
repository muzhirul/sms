from django.shortcuts import render
from rest_framework import generics, permissions
from sms.utils import CustomResponse
from .models import *
from .serializers import *
from sms.pagination import CustomPagination
from rest_framework import status
from authentication.models import Authentication
from rest_framework.response import Response
from sms.permission import check_permission
from datetime import datetime
from academic.models import ClassTeacher

# Create your views here.
class StudentList(generics.ListCreateAPIView):
    serializer_class = StudentViewSerializer
    permission_classes = [permissions.IsAuthenticated]  # Requires a valid JWT token for access
    pagination_class = CustomPagination
    
    def get_queryset(self):
        queryset = Student.objects.filter(status=True).order_by('id')
        user_id = self.request.query_params.get('user')
        try:
            user_id = self.request.query_params.get('user')
            users = Authentication.objects.get(id=user_id)
            if users.institution and users.branch:
                queryset = queryset.filter(institution=users.institution, branch=users.branch)
        except:
            institution_id = self.request.user.institution
            branch_id = self.request.user.branch
            if institution_id and branch_id:
                queryset = queryset.filter(institution=institution_id, branch=branch_id, status=True).order_by('id')
            elif branch_id:
                queryset = queryset.filter(branch=branch_id, status=True).order_by('id')
            elif institution_id:
                queryset = queryset.filter(institution=institution_id, status=True).order_by('id')
            else:
                queryset
        return queryset
    
    def list(self,request,*args, **kwargs):
        '''Check user has permission to View start'''
        permission_check = check_permission(
            self.request.user.id, 'Student Details', 'view')
        if not permission_check:
            return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to View end'''
        # serializer_class = TokenObtainPairView  # Create this serializer
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            response_data = self.get_paginated_response(serializer.data).data
        else:
            serializer = self.get_serializer(queryset, many=True)
            response_data = {
                "code": 200,
                "message": "Success",
                "data": serializer.data,
                "pagination": {
                    "next": None,
                    "previous": None,
                    "count": queryset.count(),
                },
            }

        return Response(response_data)
    
    def create(self,request,*args, **kwargs):
        '''Check user has permission to View start'''
        permission_check = check_permission(
            self.request.user.id, 'Student Admission', 'create')
        if not permission_check:
            return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to View end'''
        data = request.data
        student_data = data.copy()
        first_name = student_data.get('first_name')
        last_name = student_data.get('last_name')
        is_active = student_data.get('is_active', True) 
        user_type = student_data.get('user_type', 'STUDENT') 
        guardians_data = student_data.pop('guardians', [])
        enrolls_data = request.data.get('enroll')
        # Create the student
        serializer_class = StudentSerializer
        student_serializer = serializer_class(data=student_data)
        # student_serializer = self.get_serializer(data=student_data)
        try:
            if student_serializer.is_valid():
                student_serializer.is_valid(raise_exception=True)
                institution_data = student_serializer.validated_data.get('institution')
                branch_data = student_serializer.validated_data.get('branch')
                # If data is provided, use it; otherwise, use the values from the request user
                institution = institution_data if institution_data is not None else self.request.user.institution
                branch = branch_data if branch_data is not None else self.request.user.branch
                student = student_serializer.save(institution=institution, branch=branch)
                try:
                    std_user_data = Student.objects.values('student_no').get(id=student.id)
                    std_username = std_user_data['student_no']
                    default_password = '12345678'
                    model_name = 'Student'
                    user_count = Authentication.objects.filter(username=std_username).count()
                    if(user_count==0):
                        user = Authentication(model_name=model_name,username=std_username,first_name=first_name,last_name=last_name,user_type=user_type,is_active=is_active,institution=institution, branch=branch)
                        # Set a default password (you can change this as needed)
                        user.set_password(default_password)
                        user.save()
                        # Update the student's user_id field
                        student.user_id = user.id
                        student.save()
                    else:
                        last_username = Authentication.objects.filter(username__startswith='77').order_by('username').last()
                        # int_last_username = int(last_username)
                        int_last_username = int(last_username.username)
                        new_username = (int_last_username+1)
                        user = Authentication(model_name=model_name,username=new_username,first_name=first_name,last_name=last_name,user_type=user_type,is_active=is_active,institution=institution,branch=branch)
                        # Set a default password (you can change this as needed)
                        user.set_password(default_password)
                        user.save()
                        # Update the student's user_id field
                        student.user_id = user.id
                        student.student_no = new_username
                        student.save()
                except:
                    pass
                # Create the guardian and associate with the student
                guardians = []
                for guardian_data in guardians_data:
                    ga_first_name = guardian_data.get('first_name')
                    ga_last_name = guardian_data.get('last_name')
                    ga_is_active = guardian_data.get('is_active', True) 
                    ga_user_type = guardian_data.get('user_type', 'GUARDIAN') 
                    ga_is_guardian = guardian_data.get('is_guardian') 
                    guardian_data['student'] = student.id
                    guardian_serializer = GuardianSerializer(data=guardian_data)
                    guardian_serializer.is_valid(raise_exception=True)
                    guardian = guardian_serializer.save()
                    if ga_is_guardian:
                        try:
                            default_password = '12345678'
                            model_name = 'Guardian'
                            ga_user_data = Guardian.objects.values('guardian_no').get(id=guardian.id)
                            ga_username = ga_user_data['guardian_no']
                            ga_count = Authentication.objects.filter(username=ga_username).count()
                            if(ga_count==0):
                                ga_user = Authentication(model_name=model_name,username=ga_username,first_name=ga_first_name,last_name=ga_last_name,user_type=ga_user_type,is_active=ga_is_active,institution=institution, branch=branch)
                                # Set a default password (you can change this as needed)
                                ga_user.set_password(default_password)
                                ga_user.save()
                                # Update the Guardian's user_id field
                                guardian.user_id = ga_user.id
                                guardian.save()
                            else:
                                last_ga_username = Authentication.objects.filter(username__startswith='11').order_by('username').last()
                                int_last_ga_username = int(last_ga_username.username)
                                new_ga_username = (int_last_ga_username+1)
                                user = Authentication(model_name=model_name,username=new_ga_username,first_name=first_name,last_name=last_name,user_type=user_type,is_active=is_active,institution=institution,branch=branch)
                                # Set a default password (you can change this as needed)
                                user.set_password(default_password)
                                user.save()
                                # Update the student's user_id field
                                guardian.user_id = user.id
                                guardian.guardian_no = new_ga_username
                                guardian.save()
                        except:
                            pass
                    guardians.append(guardian)
                response_data = student_serializer.data
                response_data['guardians'] = GuardianSerializer(guardians, many=True).data
                enrolls = []
                if enrolls_data:
                    for enroll_item in enrolls_data:
                        enroll_item['student'] = student.id
                        enroll_serializer = StudentEnrollSerialize(data=enroll_item)
                        enroll_serializer.is_valid(raise_exception=True)
                        std_roll = StudentEnroll.objects.filter(status=True,section=enroll_item.get('section'),class_name=enroll_item.get('class_name'),version=enroll_item.get('version'),session=enroll_item.get('session'),institution=institution,branch=branch).order_by('roll').last()
                        if not std_roll or std_roll.roll is None:
                            class_roll = str(1)
                        else:
                            int_roll = int(std_roll.roll)
                            class_roll = str(int_roll+1)
                        enroll = enroll_serializer.save(roll=class_roll,institution=institution,branch=branch)
                        enrolls.append(enroll)
                    response_data['enroll'] = StudentEnrollSerialize(enrolls, many=True).data
        except Exception as e:
            # Handle other exceptions
            return CustomResponse(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="An error occurred during the Create", data=str(e))
            
        return Response(response_data, status=status.HTTP_201_CREATED)
       
class StudentDetail(generics.RetrieveUpdateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [permissions.IsAuthenticated]  # Requires a valid JWT token for access
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        # Customize the response format for retrieving a single instance
        return CustomResponse(code=status.HTTP_200_OK, message="Success", data=StudentViewSerializer(instance).data)
    
    def update(self, request, *args, **kwargs):
        # Get the student instance
        student = self.get_object()
        institution = self.request.user.institution
        branch = self.request.user.branch
        # Deserialize the updated student data
        student_serializer = self.get_serializer(student, data=request.data, partial=True)
        student_serializer.is_valid(raise_exception=True)
        instance = student_serializer.save()
        # Deserialize the updated guardian data
        guardian_data = request.data.get('guardians')
        enroll_data = request.data.get('enroll')
        if enroll_data:
            for enroll_item in enroll_data:
                enroll_id = enroll_item.get('id')
                if enroll_id:
                    enroll = StudentEnroll.objects.get(id=enroll_id, student=student)
                    if enroll.section.id==enroll_item.get('section') and enroll.class_name.id==enroll_item.get('class_name') and enroll.version.id==enroll_item.get('version') and enroll.session.id==enroll_item.get('session'):
                        enroll_serializer = StudentEnrollSerialize(enroll, data=enroll_item, partial=True)
                        enroll_serializer.is_valid(raise_exception=True)
                        enroll_serializer.save(institution=institution,branch=branch)
                    else:
                        std_roll = StudentEnroll.objects.filter(status=True,section=enroll_item.get('section'),class_name=enroll_item.get('class_name'),version=enroll_item.get('version'),session=enroll_item.get('session'),institution=institution,branch=branch).order_by('roll').last()
                        if not std_roll or std_roll.roll is None:
                            class_roll = str(1)
                        else:
                            int_roll = int(std_roll.roll)
                            class_roll = str(int_roll+1)
                        enroll_serializer = StudentEnrollSerialize(enroll, data=enroll_item, partial=True)
                        enroll_serializer.is_valid(raise_exception=True)
                        enroll_serializer.save(roll=class_roll,institution=institution,branch=branch)
                else:
                    std_roll = StudentEnroll.objects.filter(status=True,section=enroll_item.get('section'),class_name=enroll_item.get('class_name'),version=enroll_item.get('version'),session=enroll_item.get('session'),institution=institution,branch=branch).order_by('roll').last()
                    if not std_roll or std_roll.roll is None:
                        class_roll = str(1)
                    else:
                        int_roll = int(std_roll.roll)
                        class_roll = str(int_roll+1)
                    enroll_item['student'] = student.id
                    enroll_serializer = StudentEnrollSerialize(data=enroll_item)
                    enroll_serializer.is_valid(raise_exception=True)
                    enroll_serializer.save(roll=class_roll,institution=institution,branch=branch)

        if guardian_data:
            for guardian_item in guardian_data:
                guardian_id = guardian_item.get('id')
                if guardian_id:
                    try:
                        guardian = Guardian.objects.get(id=guardian_id, student=student)
                        guardian_serializer = GuardianSerializer(guardian, data=guardian_item, partial=True)
                        guardian_serializer.is_valid(raise_exception=True)
                        guardian_serializer.save(institution=institution,branch=branch)
                    except Guardian.DoesNotExist:
                        pass
                else:
                    ga_first_name = guardian_item.get('first_name')
                    ga_last_name = guardian_item.get('last_name')
                    ga_is_active = guardian_item.get('is_active', True) 
                    ga_user_type = guardian_item.get('user_type', 'GUARDIAN') 
                    ga_is_guardian = guardian_item.get('is_guardian')
                    # If no guardian ID provided, create a new guardian for the student
                    guardian_item['student'] = student.id
                    guardian_serializer = GuardianSerializer(data=guardian_item)
                    guardian_serializer.is_valid(raise_exception=True)
                    guardian = guardian_serializer.save(institution=institution,branch=branch)
                    if ga_is_guardian:
                        try:
                            ga_user_data = Guardian.objects.values('guardian_no').get(id=guardian.id)
                            ga_username = ga_user_data['guardian_no']
                            ga_user = Authentication(username=ga_username,first_name=ga_first_name,last_name=ga_last_name,user_type=ga_user_type,is_active=ga_is_active)
                            # Set a default password (you can change this as needed)
                            default_password = '12345678'
                            ga_user.set_password(default_password)
                            ga_user.save()
                            # Update the Guardian's user_id field
                            guardian.user_id = ga_user.id
                            guardian.save()
                        except:
                            pass
        return CustomResponse(code=status.HTTP_200_OK, message="Student updated successfully", data=StudentViewSerializer(instance).data)

class StudentImageUpload(generics.UpdateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    # Requires a valid JWT token for access
    permission_classes = [permissions.IsAuthenticated]

    def partial_update(self, request, *args, **kwargs):
        '''Check user has permission to View start'''
        permission_check = check_permission(
            self.request.user.id, 'Student Admission', 'create')
        if not permission_check:
            return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to View end'''
        # Retrieve the instance
        instance = self.get_object()

        # Get the image data from the request
        image_data = request.data.get('photo', None)

        # Validate and update the image field
        if image_data:
            instance.photo = image_data
            instance.save()
            return CustomResponse(code=status.HTTP_200_OK, message=f"Student Image Update successfully", data=None)
        return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message=f"No Image for Update", data=None)

class GuardianImageUpload(generics.UpdateAPIView):
    queryset = Guardian.objects.all()
    serializer_class = GuardianSerializer
    # Requires a valid JWT token for access
    permission_classes = [permissions.IsAuthenticated]

    def partial_update(self, request, *args, **kwargs):
        '''Check user has permission to View start'''
        permission_check = check_permission(
            self.request.user.id, 'Student Admission', 'create')
        if not permission_check:
            return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to View end'''
        # Retrieve the instance
        instance = self.get_object()

        # Get the image data from the request
        image_data = request.data.get('photo', None)

        # Validate and update the image field
        if image_data:
            instance.photo = image_data
            instance.save()
            return CustomResponse(code=status.HTTP_200_OK, message=f"Guardian Image Update successfully", data=None)
        return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message=f"No Guardian Image for Update", data=None)    

class StudentAttendanceProcess(generics.ListCreateAPIView):
     
    def list(self,request,*args, **kwargs):
        attn_date = datetime.now().date()
        student_lists = Student.objects.filter(status=True).order_by('id')
        proc_attn_daily = {}
        row_insert = 0
        day_name = attn_date.strftime('%A').lower()
        if(day_name=='friday'):
            att_type = AttendanceType.objects.get(name__iexact='weekend',status=True)
        else:
            att_type = AttendanceType.objects.get(name__iexact='absent',status=True)
        attn_id = att_type
        for std_list in student_lists:
            data_count = ProcessStAttendanceDaily.objects.filter(attn_date=attn_date,student=std_list,status=True).count()
            if data_count == 0:
                proc_attn_daily['attn_date'] = attn_date
                proc_attn_daily['student'] = std_list
                proc_attn_daily['shift'] = std_list.shift
                proc_attn_daily['student_code'] = std_list.student_no
                enroll = StudentEnroll.objects.filter(is_active=True,status=True,student=std_list).last()
                if enroll:
                    proc_attn_daily['roll'] = enroll.roll
                    proc_attn_daily['version'] = enroll.version
                    proc_attn_daily['session'] = enroll.session
                    proc_attn_daily['section'] = enroll.section
                    proc_attn_daily['class_name'] = enroll.class_name
                    proc_attn_daily['session'] = enroll.session
                    proc_attn_daily['group'] = enroll.group
                proc_attn_daily['process_date'] = datetime.now()
                proc_attn_daily['in_time'] = None
                proc_attn_daily['out_time'] = None
                proc_attn_daily['attn_type'] = attn_id
                proc_attn_daily['institution'] = std_list.institution
                proc_attn_daily['branch'] = std_list.branch
                p = ProcessStAttendanceDaily.objects.create(**proc_attn_daily)
                # std_list.last_attn_proc_date = attn_date
                # std_list.save()
                row_insert = row_insert+1
        
        return Response(f"{row_insert} insert succefully")
    
    def create(self, request, *args, **kwargs):
        data=request.data
        proc_date = data['proc_date']
        proc_date = datetime.strptime(proc_date, '%Y-%m-%d')
        day_name = proc_date.strftime('%A').lower()
        if(day_name=='friday'):
            att_type = AttendanceType.objects.get(name__iexact='weekend',status=True)
        else:
            att_type = AttendanceType.objects.get(name__iexact='absent',status=True)
        attn_id = att_type
        row_insert = 0
        proc_attn_daily = {}
        if proc_date:
            student_lists = Student.objects.filter(status=True).order_by('id')
            for std_list in student_lists:
                data_count = ProcessStAttendanceDaily.objects.filter(attn_date=proc_date,student=std_list,status=True).count()
                if data_count == 0:
                    proc_attn_daily['attn_date'] = proc_date
                    proc_attn_daily['student'] = std_list
                    proc_attn_daily['shift'] = std_list.shift
                    proc_attn_daily['student_code'] = std_list.student_no
                    enroll = StudentEnroll.objects.filter(is_active=True,status=True,student=std_list).last()
                    if enroll:
                        proc_attn_daily['roll'] = enroll.roll
                        proc_attn_daily['version'] = enroll.version
                        proc_attn_daily['session'] = enroll.session
                        proc_attn_daily['class_name'] = enroll.class_name
                        proc_attn_daily['section'] = enroll.section
                        proc_attn_daily['group'] = enroll.group
                    proc_attn_daily['process_date'] = datetime.now()
                    proc_attn_daily['in_time'] = None
                    proc_attn_daily['out_time'] = None
                    proc_attn_daily['attn_type'] = attn_id
                    proc_attn_daily['institution'] = std_list.institution
                    proc_attn_daily['branch'] = std_list.branch
                    p = ProcessStAttendanceDaily.objects.create(**proc_attn_daily)
                    # std_list.last_attn_proc_date = attn_date
                    # std_list.save()
                    row_insert = row_insert+1
        
            
        return Response(f"{row_insert} insert succefully")

class StudentAttendanceSearch(generics.CreateAPIView):
    serializer_class = ProcessStAttendanceDailySearchDailySerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        version=self.request.data['version']
        session=self.request.data['session']
        class_name=self.request.data['class_name']
        section=self.request.data['section']
        group=self.request.data['group']
        attn_date=self.request.data['attn_date']
        if group:
            queryset = ProcessStAttendanceDaily.objects.filter(attn_date=attn_date,version=version,session=session,class_name=class_name,section=section,group=group,status=True).order_by('roll')
        else:
            queryset = ProcessStAttendanceDaily.objects.filter(attn_date=attn_date,version=version,session=session,class_name=class_name,section=section,status=True).order_by('roll')
        try:
            institution_id = self.request.user.institution
            branch_id = self.request.user.branch
            # users = Authentication.objects.get(id=user_id)
            if institution_id and branch_id:
                queryset = queryset.filter(institution=institution_id, branch=branch_id, status=True).order_by('roll')
            elif branch_id:
                queryset = queryset.filter(branch=branch_id, status=True).order_by('roll')
            elif institution_id:
                queryset = queryset.filter(institution=institution_id, status=True).order_by('roll')
            else:
                queryset
        except:
            pass
        return queryset
    
    def create(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            response_data = self.get_paginated_response(serializer.data).data
        else:
            serializer = self.get_serializer(queryset, many=True)
            response_data = {
                "code": 200,
                "message": "Success",
                "data": serializer.data,
                "pagination": {
                    "next": None,
                    "previous": None,
                    "count": queryset.count(),
                },
            }

        return Response(response_data)

class StudentAttendanceUpdate(generics.UpdateAPIView):
    queryset = ProcessStAttendanceDaily.objects.filter(status=True)
    serializer_class = ProcessStAttendanceDailyUpdateDailySerializer
    permission_classes = [permissions.IsAuthenticated]  # Requires a valid JWT token for access

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        start_time = datetime.now()
        # if serializer.is_valid():
        #     instance = serializer.save(in_time=start_time)
        #     return CustomResponse(code=status.HTTP_200_OK, message="Attendance updated successfully", data=ProcessStAttendanceDailyUpdateDailySerializer(instance).data)
        try:
            if serializer.is_valid():
                instance = serializer.save(in_time=start_time)
                return CustomResponse(code=status.HTTP_200_OK, message="Attendance updated successfully", data=ProcessStAttendanceDailyUpdateDailySerializer(instance).data)
            else:
                 return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message="Validation error", data=serializer.errors)
        except Exception as e:
            # Handle other exceptions
            return CustomResponse(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="An error occurred during the update", data=str(e))

class StudentLeaveCreate(generics.CreateAPIView):
    serializer_class = StudentLeaveTransactionCreateSerializer
    permission_classes = [permissions.IsAuthenticated]  # Requires a valid JWT token for access
    pagination_class = CustomPagination

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            institution_data = serializer.validated_data.get('institution')
            apply_by = serializer.validated_data.get('apply_by')
            branch_data = serializer.validated_data.get('branch')
            start_date = serializer.validated_data.get('start_date')
            end_date = serializer.validated_data.get('end_date')
            if start_date > end_date:
                return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message="End date must be greater than or equal to start date", data=None)
            institution = institution_data if institution_data is not None else self.request.user.institution
            branch = branch_data if branch_data is not None else self.request.user.branch
            submit_status = Setup.objects.get(status=True,parent__type='APPROVAL_STATUS',type='SUBMITTED',institution=institution,branch=branch)
            if not apply_by:
                model_name = self.request.user.model_name
                username = self.request.user
                apply_by = Student.objects.get(student_no=username,status=True)
            enroll = StudentEnroll.objects.filter(is_active=True,status=True,student=apply_by).last()
            if enroll:
                roll = enroll.roll
                version = enroll.version
                session = enroll.session
                section= enroll.section
                class_name = enroll.class_name
                group= enroll.group
            if group:
                class_teacher = ClassTeacher.objects.get(status=True,institution=institution,branch=branch,version=version,session=session,section=section,class_name=class_name,group=group)
            else:
                class_teacher = ClassTeacher.objects.get(status=True,institution=institution,branch=branch,version=version,session=session,section=section,class_name=class_name)
            instance = serializer.save(app_status=submit_status,apply_by=apply_by,student_code=apply_by.student_no,shift=apply_by.shift,responsible=class_teacher.teacher,institution=institution, branch=branch,roll=roll,version=version,session=session,section=section,class_name=class_name,group=group)
            return CustomResponse(code=status.HTTP_200_OK, message="Leave created successfully", data=StudentLeaveTransactionViewSerializer(instance).data)
        
class StudentLeaveList(generics.ListAPIView):
    serializer_class = StudentLeaveTransactionListSerializer
    permission_classes = [permissions.IsAuthenticated]  # Requires a valid JWT token for access
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = StudentLeaveTransaction.objects.filter(status=True).order_by('-id')
        try:
            institution_id = self.request.user.institution
            branch_id = self.request.user.branch
            username = self.request.user
            user_id = self.request.user.id
            staff_info = Staff.objects.get(user=user_id,status=True)
            if staff_info:
                if institution_id and branch_id:
                    queryset = queryset.filter(responsible=staff_info.id,institution=institution_id, branch=branch_id, status=True).order_by('-id')
                elif branch_id:
                    queryset = queryset.filter(responsible=staff_info.id,branch=branch_id, status=True).order_by('-id')
                elif institution_id:
                    queryset = queryset.filter(responsible=staff_info.id,institution=institution_id, status=True).order_by('-id')
                else:
                    queryset
            else:
                if institution_id and branch_id:
                    queryset = queryset.filter(student_code=username,institution=institution_id, branch=branch_id, status=True).order_by('-id')
                elif branch_id:
                    queryset = queryset.filter(student_code=username,branch=branch_id, status=True).order_by('-id')
                elif institution_id:
                    queryset = queryset.filter(student_code=username,institution=institution_id, status=True).order_by('-id')
                else:
                    queryset
        except:
            pass
        return queryset
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            response_data = self.get_paginated_response(serializer.data).data
        else:
            serializer = self.get_serializer(queryset, many=True)
            response_data = {
                "code": 200,
                "message": "Success",
                "data": serializer.data,
                "pagination": {
                    "next": None,
                    "previous": None,
                    "count": queryset.count(),
                },
            }

        return Response(response_data)
    
class StudentLeaveDetails(generics.RetrieveUpdateAPIView):
    queryset = StudentLeaveTransaction.objects.all()
    serializer_class = StudentLeaveTransactionViewSerializer
    permission_classes = [permissions.IsAuthenticated]  # Requires a valid JWT token for access

    def retrieve(self, request, *args, **kwargs):
        '''Check user has permission to retrive start'''
        # permission_check = check_permission(self.request.user.id, 'Version', 'view')
        # if not permission_check:
        #     return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to retrive End'''
        
        instance = self.get_object()
        # Customize the response format for retrieving a single instance
        return CustomResponse(code=status.HTTP_200_OK, message="Success", data=StudentLeaveTransactionListSerializer(instance).data)
    
    def update(self, request, *args, **kwargs):
        '''Check user has permission to update start'''
        # permission_check = check_permission(self.request.user.id, 'Version', 'update')
        # if not permission_check:
        #     return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to retrive End'''
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        
        try:
            if serializer.is_valid():
                institution_data = serializer.validated_data.get('institution')
                branch_data = serializer.validated_data.get('branch')
                start_date = serializer.validated_data.get('start_date')
                end_date = serializer.validated_data.get('end_date')
                if start_date > end_date:
                    return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message="End date must be greater than or equal to start date", data=None)
                # If data is provided, use it; otherwise, use the values from the request user
                institution = institution_data if institution_data is not None else self.request.user.institution
                branch = branch_data if branch_data is not None else self.request.user.branch
                st = instance.app_status.title
                if (st.lower() == 'submitted'):
                    if (start_date==instance.start_date and end_date==instance.end_date):
                        instance = serializer.save()
                        return CustomResponse(code=status.HTTP_200_OK, message="Holiday Update successfully", data=StudentLeaveTransactionListSerializer(instance).data)
                    else:
                        leave_count = StudentLeaveTransaction.objects.filter(start_date=start_date,end_date=end_date,institution=institution,branch=branch,status=True).count()
                        if(leave_count==0):
                            # Perform any custom update logic here if needed
                            instance = serializer.save()
                            # Customize the response data
                            return CustomResponse(code=status.HTTP_200_OK, message="Leave Update successfully", data=StudentLeaveTransactionListSerializer(instance).data)
                        return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message=f"Leave already exits", data=serializer.errors)
                        # Customize the response format for successful update
                else:
                    return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message=f"Leave already {instance.app_status.title} ", data=StudentLeaveTransactionListSerializer(instance).data)
            else:
                # Handle validation errors
                return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message="Validation error", data=serializer.errors)
        except Exception as e:
            # Handle other exceptions
            return CustomResponse(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="An error occurred during the update", data=str(e))

class TeacherWiseStudentList(generics.ListAPIView):
    queryset = Student.objects.filter(status=True)
    serializer_class = StudentSortViewSerializer
    permission_classes = [permissions.IsAuthenticated]  # Requires a valid JWT token for access

    def get_queryset(self):
        queryset = Student.objects.filter(status=True).order_by('-id')
        username = self.request.user
        model_name = self.request.user.model_name
        institution = self.request.user.institution
        branch = self.request.user.branch
        try:
            staff_info = Staff.objects.get(staff_id=username,status=True)
            version_ids = []
            session_ids = []
            section_ids = []
            class_name_ids = []
            group_ids = []
            for cls_teacher in ClassTeacher.objects.filter(status=True,teacher=staff_info,institution=institution,branch=branch):
                session_ids.append(cls_teacher.session.id)
                version_ids.append(cls_teacher.version.id)
                class_name_ids.append(cls_teacher.class_name.id)
                section_ids.append(cls_teacher.section.id)
                if cls_teacher.group:
                    group_ids.append(cls_teacher.group.id)
                student_ids = []
                for std_id in StudentEnroll.objects.filter(status=True,is_active=True,session__in=session_ids,version__in=version_ids,class_name__in=class_name_ids,section__in=section_ids):
                    student_ids.append(std_id.student.id)
            queryset = queryset.filter(institution=institution, branch=branch, status=True,id__in=student_ids).order_by('-id')
        except:
            queryset
        return queryset

    def list(self,request,*args, **kwargs):
        '''Check user has permission to View start'''
        # permission_check = check_permission(self.request.user.id, 'Student Details', 'view')
        # if not permission_check:
        #     return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to View end'''
        # serializer_class = TokenObtainPairView  # Create this serializer
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            response_data = self.get_paginated_response(serializer.data).data
        else:
            serializer = self.get_serializer(queryset, many=True)
            response_data = {
                "code": 200,
                "message": "Success",
                "data": serializer.data,
                "pagination": {
                    "next": None,
                    "previous": None,
                    "count": queryset.count(),
                },
            }

        return Response(response_data)
