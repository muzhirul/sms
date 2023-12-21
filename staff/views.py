from django.shortcuts import render
from rest_framework import generics, permissions
from sms.utils import CustomResponse
from .models import *
from .serializers import *
from rest_framework import status
from sms.pagination import CustomPagination
from rest_framework.response import Response
from setup_app.models import *
from sms.permission import check_permission
from authentication.models import Authentication
from datetime import datetime

from django.db.models import Min, Max
from django.db.models.functions import Coalesce
from django.db.models import F
# Create your views here.

class StaffDepartmentList(generics.ListAPIView):
    serializer_class = DepartmentListSerializer
    permission_classes = [permissions.IsAuthenticated]  # Requires a valid JWT token for access
    pagination_class = CustomPagination
    
    def get_queryset(self):
        queryset = Department.objects.filter(status=True).order_by('-id')
        try:
            institution_id = self.request.user.institution
            branch_id = self.request.user.branch
            # users = Authentication.objects.get(id=user_id)
            if institution_id and branch_id:
                queryset = queryset.filter(institution=institution_id, branch=branch_id,status=True).order_by('-id')
            elif branch_id:
                queryset = queryset.filter(branch=branch_id,status=True).order_by('-id')
            elif institution_id:
                queryset = queryset.filter(institution=institution_id,status=True).order_by('-id')
            else:
                queryset            
        except:
            pass
        return queryset
        
    def list(self,request,*args, **kwargs):
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
        
class StaffDepartmentListCreate(generics.ListCreateAPIView):
    serializer_class = DepartmentSerializer
    permission_classes = [permissions.IsAuthenticated]  # Requires a valid JWT token for access
    pagination_class = CustomPagination
    
    def get_queryset(self):
        queryset = Department.objects.filter(status=True).order_by('-id')
        try:
            institution_id = self.request.user.institution
            branch_id = self.request.user.branch
            # users = Authentication.objects.get(id=user_id)
            if institution_id and branch_id:
                queryset = queryset.filter(institution=institution_id, branch=branch_id,status=True).order_by('-id')
            elif branch_id:
                queryset = queryset.filter(branch=branch_id,status=True).order_by('-id')
            elif institution_id:
                queryset = queryset.filter(institution=institution_id,status=True).order_by('-id')
            else:
                queryset            
        except:
            pass
        return queryset
        
    def list(self,request,*args, **kwargs):
        '''Check user has permission to View start'''
        permission_check = check_permission(self.request.user.id, 'Department', 'view')
        if not permission_check:
            return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to View end'''
        
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
    
    def create(self, request, *args, **kwargs):
        '''Check user has permission to Create start'''
        permission_check = check_permission(self.request.user.id, 'Department', 'create')
        if not permission_check:
            return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to Create End'''
        
        serializer = self.get_serializer(data=request.data)
        try:
            if serializer.is_valid():
                institution_data = serializer.validated_data.get('institution')
                branch_data = serializer.validated_data.get('branch')
                name = serializer.validated_data.get('name')
                # If data is provided, use it; otherwise, use the values from the request user
                institution = institution_data if institution_data is not None else self.request.user.institution
                branch = branch_data if branch_data is not None else self.request.user.branch
                department_count = Department.objects.filter(name=name,Institution=institution,branch=branch,status=True).count()
                if(department_count==0):
                    instance = serializer.save(Institution=institution,branch=branch)
                    # Customize the response data
                    return CustomResponse(code=status.HTTP_200_OK, message="Staff Department created successfully", data=DepartmentSerializer(instance).data)
                return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message=f"Staff Department {name} already exits", data=serializer.errors)
            # If the serializer is not valid, return an error response
            return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message="Validation error", data=serializer.errors)
        except Exception as e:
            # Handle other exceptions
            return CustomResponse(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="An error occurred during the Create", data=str(e))
        
class DepartmentDetail(generics.RetrieveUpdateAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [permissions.IsAuthenticated]  # Requires a valid JWT token for access
    
    def retrieve(self, request, *args, **kwargs):
        '''Check user has permission to retrive start'''
        permission_check = check_permission(self.request.user.id, 'Department', 'view')
        if not permission_check:
            return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to retrive End'''
        
        instance = self.get_object()
        # Customize the response format for retrieving a single instance
        return CustomResponse(code=status.HTTP_200_OK, message="Success", data=DepartmentSerializer(instance).data)

    def update(self, request, *args, **kwargs):
        '''Check user has permission to update start'''
        permission_check = check_permission(self.request.user.id, 'Department', 'update')
        if not permission_check:
            return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to retrive End'''
        
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        
        try:
            if serializer.is_valid():
                institution_data = serializer.validated_data.get('institution')
                branch_data = serializer.validated_data.get('branch')
                name = serializer.validated_data.get('name')
                # If data is provided, use it; otherwise, use the values from the request user
                institution = institution_data if institution_data is not None else self.request.user.institution
                branch = branch_data if branch_data is not None else self.request.user.branch
                department_count = Department.objects.filter(name=name,Institution=institution,branch=branch,status=True).count()
                if(department_count==0):
                    # Perform any custom update logic here if needed
                    instance = serializer.save()
                    # Customize the response data
                    return CustomResponse(code=status.HTTP_200_OK, message="Department Updated successfully", data=DepartmentSerializer(instance).data)
                return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message=f"Department {name} already exits", data=serializer.errors)
                # Customize the response format for successful update
            else:
                # Handle validation errors
                return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message="Validation error", data=serializer.errors)
        except Exception as e:
            # Handle other exceptions
            return CustomResponse(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="An error occurred during the update", data=str(e))

class DepartmentDelete(generics.UpdateAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [permissions.IsAuthenticated]  # Requires a valid JWT token for access
    
    def partial_update(self, request, *args, **kwargs):
        '''Check user has permission to Delete start'''
        permission_check = check_permission(self.request.user.id, 'Department', 'delete')
        if not permission_check:
            return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to Delete End'''
        
        instance = self.get_object()
        if not instance.status:
            return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message=f"Department {instance.name} already Deleted", data=None)
        # Update the "status" field to False
        instance.status = False
        instance.save()
        # Customize the response format for successful update
        return CustomResponse(code=status.HTTP_200_OK, message=f"Department {instance.name} Delete successfully", data=None)

class StaffDesignationListCreate(generics.ListCreateAPIView):
    serializer_class = DesignationSerializer
    permission_classes = [permissions.IsAuthenticated]  # Requires a valid JWT token for access
    pagination_class = CustomPagination
    
    def get_queryset(self):
        queryset = Designation.objects.filter(status=True).order_by('-id')
        try:
            institution_id = self.request.user.institution
            branch_id = self.request.user.branch
            # users = Authentication.objects.get(id=user_id)
            if institution_id and branch_id:
                queryset = queryset.filter(institution=institution_id, branch=branch_id,status=True).order_by('-id')
            elif branch_id:
                queryset = queryset.filter(branch=branch_id,status=True).order_by('-id')
            elif institution_id:
                queryset = queryset.filter(institution=institution_id,status=True).order_by('-id')
            else:
                queryset            
        except:
            pass
        return queryset
        
    def list(self,request,*args, **kwargs):
        '''Check user has permission to View start'''
        permission_check = check_permission(self.request.user.id, 'Designation', 'view')
        if not permission_check:
            return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to View end'''
        
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
    
    def create(self, request, *args, **kwargs):
        '''Check user has permission to Create start'''
        permission_check = check_permission(self.request.user.id, 'Designation', 'create')
        if not permission_check:
            return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to Create End'''
        
        serializer = self.get_serializer(data=request.data)
        try:
            if serializer.is_valid():
                institution_data = serializer.validated_data.get('institution')
                branch_data = serializer.validated_data.get('branch')
                name = serializer.validated_data.get('name')
                # If data is provided, use it; otherwise, use the values from the request user
                institution = institution_data if institution_data is not None else self.request.user.institution
                branch = branch_data if branch_data is not None else self.request.user.branch
                department_count = Designation.objects.filter(name=name,Institution=institution,branch=branch,status=True).count()
                if(department_count==0):
                    instance = serializer.save(Institution=institution,branch=branch)
                    # Customize the response data
                    return CustomResponse(code=status.HTTP_200_OK, message="Staff Designation created successfully", data=DesignationSerializer(instance).data)
                return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message=f"Staff Designation {name} already exits", data=serializer.errors)
            # If the serializer is not valid, return an error response
            return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message="Validation error", data=serializer.errors)
        except Exception as e:
            # Handle other exceptions
            return CustomResponse(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="An error occurred during the Create", data=str(e))

class StaffDesignationList(generics.ListAPIView):
    serializer_class = DesignationListSerializer
    permission_classes = [permissions.IsAuthenticated]  # Requires a valid JWT token for access
    pagination_class = CustomPagination
    
    def get_queryset(self):
        queryset = Designation.objects.filter(status=True).order_by('-id')
        try:
            institution_id = self.request.user.institution
            branch_id = self.request.user.branch
            # users = Authentication.objects.get(id=user_id)
            if institution_id and branch_id:
                queryset = queryset.filter(institution=institution_id, branch=branch_id,status=True).order_by('-id')
            elif branch_id:
                queryset = queryset.filter(branch=branch_id,status=True).order_by('-id')
            elif institution_id:
                queryset = queryset.filter(institution=institution_id,status=True).order_by('-id')
            else:
                queryset            
        except:
            pass
        return queryset
        
    def list(self,request,*args, **kwargs):
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

class DesignationDetail(generics.RetrieveUpdateAPIView):
    queryset = Designation.objects.all()
    serializer_class = DesignationSerializer
    permission_classes = [permissions.IsAuthenticated]  # Requires a valid JWT token for access
    
    def retrieve(self, request, *args, **kwargs):
        '''Check user has permission to retrive start'''
        permission_check = check_permission(self.request.user.id, 'Designation', 'view')
        if not permission_check:
            return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to retrive End'''
        
        instance = self.get_object()
        # Customize the response format for retrieving a single instance
        return CustomResponse(code=status.HTTP_200_OK, message="Success", data=DesignationSerializer(instance).data)

    def update(self, request, *args, **kwargs):
        '''Check user has permission to update start'''
        permission_check = check_permission(self.request.user.id, 'Designation', 'update')
        if not permission_check:
            return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to retrive End'''
        
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        
        try:
            if serializer.is_valid():
                institution_data = serializer.validated_data.get('institution')
                branch_data = serializer.validated_data.get('branch')
                name = serializer.validated_data.get('name')
                # If data is provided, use it; otherwise, use the values from the request user
                institution = institution_data if institution_data is not None else self.request.user.institution
                branch = branch_data if branch_data is not None else self.request.user.branch
                department_count = Designation.objects.filter(name=name,Institution=institution,branch=branch,status=True).count()
                if(department_count==0):
                    # Perform any custom update logic here if needed
                    instance = serializer.save()
                    # Customize the response data
                    return CustomResponse(code=status.HTTP_200_OK, message="Designation Updated successfully", data=DesignationSerializer(instance).data)
                return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message=f"Designation {name} already exits", data=serializer.errors)
                # Customize the response format for successful update
            else:
                # Handle validation errors
                return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message="Validation error", data=serializer.errors)
        except Exception as e:
            # Handle other exceptions
            return CustomResponse(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="An error occurred during the update", data=str(e))

class DesignationDelete(generics.UpdateAPIView):
    queryset = Designation.objects.all()
    serializer_class = DesignationSerializer
    permission_classes = [permissions.IsAuthenticated]  # Requires a valid JWT token for access
    
    def partial_update(self, request, *args, **kwargs):
        '''Check user has permission to Delete start'''
        permission_check = check_permission(self.request.user.id, 'Designation', 'delete')
        if not permission_check:
            return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to Delete End'''
        
        instance = self.get_object()
        if not instance.status:
            return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message=f"Designation {instance.name} already Deleted", data=None)
        # Update the "status" field to False
        instance.status = False
        instance.save()
        # Customize the response format for successful update
        return CustomResponse(code=status.HTTP_200_OK, message=f"Designation {instance.name} Delete successfully", data=None)

'''For Staff'''

class staffTeacherListView(generics.ListAPIView):
    serializer_class = StaffTeacherViewSerializer
    permission_classes = [permissions.IsAuthenticated]  # Requires a valid JWT token for access
    pagination_class = CustomPagination
    
    def get_queryset(self):
        queryset = Staff.objects.filter(role__name__iexact='teacher',status=True).order_by('-id')
        try:
            institution_id = self.request.user.institution
            branch_id = self.request.user.branch
            # users = Authentication.objects.get(id=user_id)
            if institution_id and branch_id:
                queryset = queryset.filter(institution=institution_id, branch=branch_id,status=True).order_by('-id')
            elif branch_id:
                queryset = queryset.filter(branch=branch_id,status=True).order_by('-id')
            elif institution_id:
                queryset = queryset.filter(institution=institution_id,status=True).order_by('-id')
            else:
                queryset            
        except:
            pass
        return queryset
    
    def list(self,request,*args, **kwargs):
        '''Check user has permission to View start'''
        # permission_check = check_permission(self.request.user.id, 'Staff Shift', 'view')
        # if not permission_check:
        #     return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to View end'''
        
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


class staffCreateView(generics.CreateAPIView):
    serializer_class = staffCreateSerializer
    permission_classes = [permissions.IsAuthenticated]  # Requires a valid JWT token for access
    pagination_class = CustomPagination
    
    def get_queryset(self):
        queryset = Staff.objects.filter(status=True).order_by('-id')
        try:
            institution_id = self.request.user.institution
            branch_id = self.request.user.branch
            # users = Authentication.objects.get(id=user_id)
            if institution_id and branch_id:
                queryset = queryset.filter(institution=institution_id, branch=branch_id,status=True).order_by('-id')
            elif branch_id:
                queryset = queryset.filter(branch=branch_id,status=True).order_by('-id')
            elif institution_id:
                queryset = queryset.filter(institution=institution_id,status=True).order_by('-id')
            else:
                queryset            
        except:
            pass
        return queryset
    
    def create(self,request,*args, **kwargs):
        data = request.data
        staff_data = data.copy()
        first_name = staff_data.get('first_name')
        last_name = staff_data.get('last_name')
        is_active = staff_data.get('is_active', True) 
        user_type = staff_data.get('user_type', '') 
        # education_datas = staff_data.pop('staff_education', [])
        staff_serializer = self.get_serializer(data=staff_data)
        try:
            if staff_serializer.is_valid():
                staff_serializer.is_valid(raise_exception=True)
                institution_data = staff_serializer.validated_data.get('institution')
                branch_data = staff_serializer.validated_data.get('branch')
                # If data is provided, use it; otherwise, use the values from the request user
                institution = institution_data if institution_data is not None else self.request.user.institution
                branch = branch_data if branch_data is not None else self.request.user.branch
                staff = staff_serializer.save(institution=institution,branch=branch)
                default_password = '12345678'
                Leaves_info = LeaveType.objects.filter(status=True,institution=institution,branch=branch,is_active=True)
                for Leave_data in Leaves_info:
                    if staff.doj:
                        start_date = datetime(staff.doj.year,1,1)
                        end_date = datetime(staff.doj.year,12,31)
                        remain_month = 13-staff.doj.month
                    else:
                        start_date = datetime(datetime.now().year,1,1)
                        end_date = datetime(datetime.now().year,12,31)
                        remain_month = 13-datetime.now().month
                    actual_leave_day = round((Leave_data.max_days/12)*remain_month)    
                    leave = StaffLeave(start_date=start_date,end_date=end_date,leave_days=actual_leave_day,institution=institution,branch=branch)
                    leave.staff_id = staff.id
                    leave.leave_type_id = Leave_data.id
                    leave.save()
                try:
                    std_user_data = Staff.objects.values('staff_id').get(id=staff.id)
                    std_username = std_user_data['staff_id']
                    user_count = Authentication.objects.filter(username=std_username).count()
                    if (user_count==0):
                        user = Authentication(username=std_username,first_name=first_name,last_name=last_name,user_type=user_type,is_active=is_active,institution=institution,branch=branch)
                        # Set a default password (you can change this as needed)
                        user.set_password(default_password)
                        user.save()
                        # Update the student's user_id field
                        staff.user_id = user.id
                        staff.save()
                    else:
                        last_username = Authentication.objects.filter(username__startswith='99').order_by('username').last()
                        # int_last_username = int(last_username)
                        int_last_username = int(last_username.username)
                        new_username = (int_last_username+1)
                        user = Authentication(username=new_username,first_name=first_name,last_name=last_name,user_type=user_type,is_active=is_active,institution=institution,branch=branch)
                        # Set a default password (you can change this as needed)
                        user.set_password(default_password)
                        user.save()
                        # Update the student's user_id field
                        staff.user_id = user.id
                        staff.staff_id = new_username
                        staff.save()
                except:
                    pass
                # staff_educations = []
                # for education_data in education_datas:
                #     education_data['staff'] = staff.id
                #     education_serializer = EducationSerializer(data=education_data)
                #     education_serializer.is_valid(raise_exception=True)
                #     education = education_serializer.save()
                #     staff_educations.append(education)
                # response_data = staff_serializer.data
        except Exception as e:
            # Handle other exceptions
            return CustomResponse(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="An error occurred during the Create", data=str(e))
        return CustomResponse(code=status.HTTP_200_OK, message="Staff created successfully", data=staff_serializer.data)    

class staffListView(generics.ListAPIView):
    serializer_class = staffSerializer2
    permission_classes = [permissions.IsAuthenticated]  # Requires a valid JWT token for access
    pagination_class = CustomPagination
    
    def get_queryset(self):
        queryset = Staff.objects.filter(status=True).order_by('-id')
        try:
            institution_id = self.request.user.institution
            branch_id = self.request.user.branch
            # users = Authentication.objects.get(id=user_id)
            if institution_id and branch_id:
                queryset = queryset.filter(institution=institution_id, branch=branch_id,status=True).order_by('-id')
            elif branch_id:
                queryset = queryset.filter(branch=branch_id,status=True).order_by('-id')
            elif institution_id:
                queryset = queryset.filter(institution=institution_id,status=True).order_by('-id')
            else:
                queryset            
        except:
            pass
        return queryset
    
    def list(self,request,*args, **kwargs):
        '''Check user has permission to View start'''
        # permission_check = check_permission(self.request.user.id, 'Staff Shift', 'view')
        # if not permission_check:
        #     return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to View end'''
        
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

class staffDetailView(generics.RetrieveUpdateAPIView):
    queryset = Staff.objects.all()
    serializer_class = staffSerializer
    permission_classes = [permissions.IsAuthenticated]  # Requires a valid JWT token for access

    def retrieve(self, request, *args, **kwargs):
        '''Check user has permission to retrive start'''
        # permission_check = check_permission(self.request.user.id, 'Shift', 'view')
        # if not permission_check:
        #     return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to retrive End'''
        instance = self.get_object()
        # Customize the response format for retrieving a single instance
        return CustomResponse(code=status.HTTP_200_OK, message="Success", data=staffSerializer2(instance).data)
    
    def update(self, request, *args, **kwargs):
        # Get the student instance
        staff = self.get_object()
        # Deserialize the updated student data
        staff_serializer = self.get_serializer(staff, data=request.data, partial=True)
        staff_serializer.is_valid(raise_exception=True)
        instance = staff_serializer.save()
        return CustomResponse(code=status.HTTP_200_OK, message="Staff information updated successfully", data=staffSerializer2(instance).data)

class StaffImageUpload(generics.UpdateAPIView):
    queryset = Staff.objects.all()
    serializer_class = staffSerializer
    # Requires a valid JWT token for access
    permission_classes = [permissions.IsAuthenticated]

    def partial_update(self, request, *args, **kwargs):
        '''Check user has permission to View start'''
        # permission_check = check_permission(
        #     self.request.user.id, 'Student Admission', 'create')
        # if not permission_check:
        #     return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to View end'''
        # Retrieve the instance
        instance = self.get_object()

        # Get the image data from the request
        image_data = request.data.get('photo', None)

        # Validate and update the image field
        if image_data:
            instance.photo = image_data
            instance.save()
            return CustomResponse(code=status.HTTP_200_OK, message=f"Staff Image Update successfully", data=None)
        return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message=f"No Image for Update", data=None)

class StaffShiftListCreate(generics.ListCreateAPIView):
    # queryset = Version.objects.filter(status=True).order_by('id')
    serializer_class = StaffShiftSerializer
    permission_classes = [permissions.IsAuthenticated]  # Requires a valid JWT token for access
    pagination_class = CustomPagination
    
    def get_queryset(self):
        queryset = StaffShift.objects.filter(status=True).order_by('-id')
        try:
            institution_id = self.request.user.institution
            branch_id = self.request.user.branch
            # users = Authentication.objects.get(id=user_id)
            if institution_id and branch_id:
                queryset = queryset.filter(institution=institution_id, branch=branch_id,status=True).order_by('-id')
            elif branch_id:
                queryset = queryset.filter(branch=branch_id,status=True).order_by('-id')
            elif institution_id:
                queryset = queryset.filter(institution=institution_id,status=True).order_by('-id')
            else:
                queryset            
        except:
            pass
        return queryset
        
    def list(self,request,*args, **kwargs):
        '''Check user has permission to View start'''
        permission_check = check_permission(self.request.user.id, 'Shift', 'view')
        if not permission_check:
            return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to View end'''
        
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
    
    def create(self, request, *args, **kwargs):
        '''Check user has permission to View start'''
        permission_check = check_permission(self.request.user.id, 'Shift', 'create')
        if not permission_check:
            return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to View end'''
        serializer = self.get_serializer(data=request.data)
        try:
            if serializer.is_valid():
                institution_data = serializer.validated_data.get('Institution')
                branch_data = serializer.validated_data.get('branch')
                start_time = serializer.validated_data.get('start_time')
                end_time = serializer.validated_data.get('end_time')
                name = serializer.validated_data.get('name')
                # If data is provided, use it; otherwise, use the values from the request user
                institution_info = institution_data if institution_data is not None else self.request.user.institution
                branch_info = branch_data if branch_data is not None else self.request.user.branch
                session_count = StaffShift.objects.filter(start_time=start_time,end_time=end_time,institution=institution_info,branch=branch_info,status=True).count()
                if(session_count==0):
                    instance = serializer.save(institution=institution_info, branch=branch_info)
                    # Customize the response data
                    return CustomResponse(code=status.HTTP_200_OK, message="Staff Shift created successfully", data=StaffShiftSerializer(instance).data)
                return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message=f"Staff Shift {name} already exits", data=serializer.errors)
            # If the serializer is not valid, return an error response
            return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message="Validation error", data=serializer.errors)
        except Exception as e:
            # Handle other exceptions
            return CustomResponse(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="An error occurred during the Create", data=str(e))

class StaffShiftDetail(generics.RetrieveUpdateAPIView):
    queryset = StaffShift.objects.all()
    serializer_class = StaffShiftSerializer
    permission_classes = [permissions.IsAuthenticated]  # Requires a valid JWT token for access
    
    def retrieve(self, request, *args, **kwargs):
        '''Check user has permission to retrive start'''
        permission_check = check_permission(self.request.user.id, 'Shift', 'view')
        if not permission_check:
            return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to retrive End'''
        instance = self.get_object()
        # Customize the response format for retrieving a single instance
        return CustomResponse(code=status.HTTP_200_OK, message="Success", data=StaffShiftSerializer(instance).data)

    def update(self, request, *args, **kwargs):
        '''Check user has permission to update start'''
        permission_check = check_permission(self.request.user.id, 'Shift', 'update')
        if not permission_check:
            return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to retrive End'''
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        
        try:
            if serializer.is_valid():
                institution_data = serializer.validated_data.get('institution')
                branch_data = serializer.validated_data.get('branch')
                start_time = serializer.validated_data.get('start_time')
                end_time = serializer.validated_data.get('end_time')
                name = serializer.validated_data.get('name')
                institution_info = institution_data if institution_data is not None else self.request.user.institution
                branch_info = branch_data if branch_data is not None else self.request.user.branch
                session_count = StaffShift.objects.filter(start_time=start_time,end_time=end_time,institution=institution_info,branch=branch_info,status=True).count()
                if (session_count==0):
                    # Perform any custom update logic here if needed
                    instance = serializer.save()
                    # Customize the response format for successful update
                    return CustomResponse(code=status.HTTP_200_OK, message="Shift updated successfully", data=StaffShiftSerializer(instance).data)
                return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message=f"Shift {name} already exits", data=serializer.errors)
            else:
                # Handle validation errors
                return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message="Validation error", data=serializer.errors)
        except Exception as e:
            # Handle other exceptions
            return CustomResponse(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="An error occurred during the update", data=str(e))

class StaffShiftDelete(generics.UpdateAPIView):
    queryset = StaffShift.objects.all()
    serializer_class = StaffShiftSerializer
    permission_classes = [permissions.IsAuthenticated]  # Requires a valid JWT token for access
    
    def partial_update(self, request, *args, **kwargs):
        '''Check user has permission to Delete start'''
        permission_check = check_permission(self.request.user.id, 'Shift', 'delete')
        if not permission_check:
            return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to Delete End'''
        
        instance = self.get_object()
        if not instance.status:
            return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message=f"Shift {instance.name} already Deleted", data=None)
        # Update the "status" field to False
        instance.status = False
        instance.save()
        # Customize the response format for successful update
        return CustomResponse(code=status.HTTP_200_OK, message=f"Shift {instance.name} Delete successfully", data=None)

class StaffShiftList(generics.ListAPIView):
    serializer_class = StaffShiftListSerializer2
    permission_classes = [permissions.IsAuthenticated]  # Requires a valid JWT token for access
    pagination_class = CustomPagination
    
    def get_queryset(self):
        queryset = StaffShift.objects.filter(status=True).order_by('-id')
        try:
            institution_id = self.request.user.institution
            branch_id = self.request.user.branch
            # users = Authentication.objects.get(id=user_id)
            if institution_id and branch_id:
                queryset = queryset.filter(institution=institution_id, branch=branch_id,status=True).order_by('-id')
            elif branch_id:
                queryset = queryset.filter(branch=branch_id,status=True).order_by('-id')
            elif institution_id:
                queryset = queryset.filter(institution=institution_id,status=True).order_by('-id')
            else:
                queryset            
        except:
            pass
        return queryset
        
    def list(self,request,*args, **kwargs):
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

class StaffAttendanceProcess(generics.ListCreateAPIView):
     
    def list(self,request,*args, **kwargs):
        attn_date = datetime.now().date()
        staff_lists = Staff.objects.filter(status=True).order_by('id')
        proc_attn_daily = {}
        row_insert = 0
        att_type = AttendanceType.objects.get(name__iexact='absent',status=True)
        attn_id = att_type
        for staff_list in staff_lists:
            data_count = ProcessAttendanceDaily.objects.filter(attn_date=attn_date,staff=staff_list,status=True).count()
            if data_count == 0:
                proc_attn_daily['attn_date'] = attn_date
                proc_attn_daily['staff'] = staff_list
                proc_attn_daily['shift'] = staff_list.shift
                proc_attn_daily['staff_code'] = staff_list.staff_id
                payroll = StaffPayroll.objects.filter(is_active=True,status=True,staff=staff_list).last()
                if payroll:
                    proc_attn_daily['con_type'] = payroll.contract_type
                proc_attn_daily['attn_type'] = None
                proc_attn_daily['process_date'] = datetime.now()
                proc_attn_daily['in_time'] = None
                proc_attn_daily['out_time'] = None
                proc_attn_daily['attn_type'] = attn_id
                proc_attn_daily['role'] = staff_list.role
                proc_attn_daily['designation'] = staff_list.designation
                proc_attn_daily['department'] = staff_list.department
                proc_attn_daily['institution'] = staff_list.institution
                proc_attn_daily['branch'] = staff_list.branch
                p = ProcessAttendanceDaily.objects.create(**proc_attn_daily)
                staff_list.last_attn_proc_date = attn_date
                staff_list.save()
                row_insert = row_insert+1
        
        return Response(f"{row_insert} insert succefully")
    
    def create(self, request, *args, **kwargs):
        data=request.data
        proc_date = data['proc_date']
        att_type = AttendanceType.objects.get(name__iexact='absent',status=True)
        attn_id = att_type
        row_insert = 0
        if proc_date:
            staff_lists = Staff.objects.filter(status=True).order_by('id')
            for staff_list in staff_lists:
                data_count = ProcessAttendanceDaily.objects.filter(attn_date=proc_date,staff=staff_list,status=True).count()
                proc_attn_daily = {}
                if data_count == 0:
                    proc_attn_daily['attn_date'] = proc_date
                    proc_attn_daily['staff'] = staff_list
                    proc_attn_daily['shift'] = staff_list.shift
                    proc_attn_daily['staff_code'] = staff_list.staff_id
                    payroll = StaffPayroll.objects.filter(is_active=True,status=True,staff=staff_list).last()
                    if payroll:
                        proc_attn_daily['con_type'] = payroll.contract_type
                    proc_attn_daily['attn_type'] = None
                    proc_attn_daily['process_date'] = datetime.now()
                    proc_attn_daily['in_time'] = None
                    proc_attn_daily['out_time'] = None
                    proc_attn_daily['attn_type'] = attn_id
                    proc_attn_daily['role'] = staff_list.role
                    proc_attn_daily['designation'] = staff_list.designation
                    proc_attn_daily['department'] = staff_list.department
                    proc_attn_daily['institution'] = staff_list.institution
                    proc_attn_daily['branch'] = staff_list.branch
                    p = ProcessAttendanceDaily.objects.create(**proc_attn_daily)
                    staff_list.last_attn_proc_date = proc_date
                    staff_list.save()
                    row_insert = row_insert+1
            
        return Response(f"{row_insert} insert succefully")
         
class StaffAttendanceEntry(generics.CreateAPIView):
    serializer_class = AttendanceDailyCreateRawSerializer
    permission_classes = [permissions.IsAuthenticated]  # Requires a valid JWT token for access
    pagination_class = CustomPagination

    def create(self, request, *args, **kwargs):
        try:
            attn_daily_data = request.data.get("raw_atten", [])
            serializer = self.get_serializer(data=attn_daily_data, many=True)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return CustomResponse(code=status.HTTP_200_OK, message="Staff Manual Attendance created successfully", data=serializer.data)
        except Exception as e:
            # Handle other exceptions
            return CustomResponse(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="An error occurred during the Create", data=str(e))

class StaffAttendanceUpdateProcess(generics.ListAPIView):

    def list(self,request,*args, **kwargs):
        attn_date = datetime.now().date()
        # attn_raw_datas = AttendanceDailyRaw.objects.filter(attn_date=attn_date,staff__isnull=False,is_active=True, status=True).order_by('-trnsc_time')
        attn_raw_datas = AttendanceDailyRaw.objects.filter(attn_date=attn_date,staff__isnull=False,is_active=True, status=True).values('staff', 'attn_date').annotate(
                                    in_time=Coalesce(Min('trnsc_time'), F('attn_date')),
                                    out_time=Coalesce(Max('trnsc_time'), F('attn_date'))
                                )
        for attn_raw_data in attn_raw_datas:
            print(attn_raw_data)
            # print(attn_raw_data['staff'])
            in_datetime = attn_raw_data['in_time']
            out_datetime = attn_raw_data['out_time']
            daily_attn = ProcessAttendanceDaily.objects.get(attn_date=attn_raw_data['attn_date'],staff=attn_raw_data['staff'],is_active=True,status=True)
            # print(daily_attn.shift.start_time)
            if daily_attn:
                shift_start_time = daily_attn.shift.start_time
                shift_end_time = daily_attn.shift.end_time
                in_time = in_datetime.time()
                out_time = out_datetime.time()
                if in_time <= shift_start_time:
                    att_type = AttendanceType.objects.get(name__iexact='present',status=True)
                    attn_id = att_type
                elif in_time > shift_start_time:
                    att_type = AttendanceType.objects.get(name__iexact='late',status=True)
                    attn_id = att_type
                else:
                    att_type = AttendanceType.objects.get(name__iexact='absent',status=True)
                    attn_id = att_type
                daily_attn.in_time = in_datetime
                daily_attn.out_time = out_datetime
                daily_attn.attn_type = attn_id
                daily_attn.save()
                print(in_time,out_time,attn_id)
            # if daily_attn:
            #     if attn_raw_data.attn_type == 'IN':
            #         print('In Process')
            #         shift_start_time = daily_attn.shift.start_time
            #         # print(shift_start_time)
            #         in_time = attn_raw_data.trnsc_time.time()
            #         if in_time <= shift_start_time:
            #             att_type = AttendanceType.objects.get(name__iexact='present',status=True)
            #             attn_id = att_type
            #         elif in_time > shift_start_time:
            #             att_type = AttendanceType.objects.get(name__iexact='late',status=True)
            #             attn_id = att_type
            #         else:
            #             att_type = AttendanceType.objects.get(name__iexact='absent',status=True)
            #             attn_id = att_type
            #         # print('====')
            #         daily_attn.in_time = attn_raw_data.trnsc_time
            #         daily_attn.attn_type = attn_id
            #         daily_attn.save()
            #         # print(daily_attn)
            #     elif attn_raw_data.attn_type == 'OUT':
            #         print('Out Process')
            #         out_time = attn_raw_data.trnsc_time.time()
            #         daily_attn.out_time = attn_raw_data.trnsc_time
            #         daily_attn.save()
        return Response('okay')
