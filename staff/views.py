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

class staffCreateView(generics.CreateAPIView):
    serializer_class = staffSerializer
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
        education_datas = staff_data.pop('staff_education', [])
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
                try:
                    std_user_data = Staff.objects.values('staff_id').get(id=staff.id)
                    std_username = std_user_data['staff_id']
                    user_count = Authentication.objects.filter(username=std_username).count()
                    print(user_count)
                    if (user_count==0):
                        user = Authentication(username=std_username,first_name=first_name,last_name=last_name,user_type=user_type,is_active=is_active,institution=institution,branch=branch)
                            # Set a default password (you can change this as needed)
                        default_password = '12345678'
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
                        default_password = '12345678'
                        user.set_password(default_password)
                        user.save()
                            # Update the student's user_id field
                        staff.user_id = user.id
                        staff.staff_id = new_username
                        staff.save()
                except:
                    pass
                staff_educations = []
                for education_data in education_datas:
                    education_data['staff'] = staff.id
                    education_serializer = EducationSerializer(data=education_data)
                    education_serializer.is_valid(raise_exception=True)
                    education = education_serializer.save()
                    staff_educations.append(education)
                response_data = staff_serializer.data
        except Exception as e:
            # Handle other exceptions
            return CustomResponse(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="An error occurred during the Create", data=str(e))
            
        return Response(response_data, status=status.HTTP_201_CREATED)

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
        permission_check = check_permission(self.request.user.id, 'Staff Shift', 'view')
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
        permission_check = check_permission(self.request.user.id, 'Staff Shift', 'create')
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
        permission_check = check_permission(self.request.user.id, 'Session', 'view')
        if not permission_check:
            return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to retrive End'''
        instance = self.get_object()
        # Customize the response format for retrieving a single instance
        return CustomResponse(code=status.HTTP_200_OK, message="Success", data=StaffShiftSerializer(instance).data)

    def update(self, request, *args, **kwargs):
        '''Check user has permission to update start'''
        permission_check = check_permission(self.request.user.id, 'Session', 'update')
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
                    return CustomResponse(code=status.HTTP_200_OK, message="Session updated successfully", data=StaffShiftSerializer(instance).data)
                return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message=f"Session {name} already exits", data=serializer.errors)
            else:
                # Handle validation errors
                return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message="Validation error", data=serializer.errors)
        except Exception as e:
            # Handle other exceptions
            return CustomResponse(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="An error occurred during the update", data=str(e))
 
