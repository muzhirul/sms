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
from django.shortcuts import get_object_or_404
from django.db.models import Q
import requests
from datetime import timedelta
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

class StaffSearchList(generics.CreateAPIView):
    serializer_class = StaffTeacherViewSerializer
    permission_classes = [permissions.IsAuthenticated]  # Requires a valid JWT token for access
    pagination_class = CustomPagination

    def get_queryset(self):
        # Get the role ID from the URL parameter
        staff_ids = self.request.data.get('staff_id', [])
        queryset = Staff.objects.filter(id__in=staff_ids)
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

class staffRoleBaseSataffListView(generics.ListAPIView):
    serializer_class = StaffTeacherViewSerializer
    permission_classes = [permissions.IsAuthenticated]  # Requires a valid JWT token for access
    pagination_class = CustomPagination

    def get_queryset(self):
        # Get the role ID from the URL parameter
        role_id = int(self.kwargs['role_id'])
        if(role_id==0):
            queryset = Staff.objects.filter(status=True)
        else:
            queryset = Staff.objects.filter(role__id=role_id,status=True)
        try:
            institution_id = self.request.user.institution
            branch_id = self.request.user.branch
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

class staffLessDtlListView(generics.ListAPIView):
    serializer_class = StaffTeacherViewSerializer
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
                model_name = 'Staff'
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
                        user = Authentication(model_name=model_name,username=std_username,first_name=first_name,last_name=last_name,user_type=user_type,is_active=is_active,institution=institution,branch=branch)
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
                        user = Authentication(model_name=model_name,username=new_username,first_name=first_name,last_name=last_name,user_type=user_type,is_active=is_active,institution=institution,branch=branch)
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
        day_name = attn_date.strftime('%A').lower()
        if(day_name=='friday'):
            att_type = AttendanceType.objects.get(name__iexact='weekend',status=True)
        else:
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
        proc_date = datetime.strptime(proc_date, '%Y-%m-%d')
        day_name = proc_date.strftime('%A').lower()
        if(day_name=='friday'):
            att_type = AttendanceType.objects.get(name__iexact='weekend',status=True)
        else:
            att_type = AttendanceType.objects.get(name__iexact='absent',status=True)
        # att_type = AttendanceType.objects.get(name__iexact='absent',status=True)
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
            institution_id = self.request.user.institution.id
            branch_id = self.request.user.branch.id
            attn_daily_data = request.data.get("raw_atten", [])
            for item in attn_daily_data:
                item["institution"] = institution_id
                item["branch"] = branch_id
            print(attn_daily_data)
            serializer = self.get_serializer(data=attn_daily_data, many=True)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return CustomResponse(code=status.HTTP_200_OK, message="Staff Manual Attendance created successfully", data=serializer.data)
        except Exception as e:
            # Handle other exceptions
            return CustomResponse(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="An error occurred during the Create", data=str(e))

class staffRawAttendanceList(generics.ListAPIView):
    serializer_class = AttendanceDailyRawViewSerializer
    permission_classes = [permissions.IsAuthenticated]  # Requires a valid JWT token for access
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = AttendanceDailyRaw.objects.filter(status=True).order_by('-id')
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

class staffSpecificRawAttendance(generics.CreateAPIView):
    serializer_class = AttendanceDailyRawViewSerializer
    permission_classes = [permissions.IsAuthenticated]  # Requires a valid JWT token for access
    pagination_class = CustomPagination

    def get_queryset(self):
        staff_id = self.request.data.get('staff_id')
        from_date = self.request.data.get('from_date')
        to_date = self.request.data.get('to_date')
        queryset = AttendanceDailyRaw.objects.filter(staff__id=staff_id,attn_date__range=[from_date, to_date],status=True).order_by('-id')
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

class StaffAttendanceUpdateProcess(generics.ListCreateAPIView):

    def list(self,request,*args, **kwargs):
        attn_date = datetime.now().date()
        try:
            attn_raw_datas = AttendanceDailyRaw.objects.filter(attn_date=attn_date,staff__isnull=False,is_active=True, status=True).values('staff', 'attn_date').annotate(
                                        in_time=Coalesce(Min('trnsc_time'), F('attn_date')),
                                        out_time=Coalesce(Max('trnsc_time'), F('attn_date'))
                                    )
            for attn_raw_data in attn_raw_datas:
                in_datetime = attn_raw_data['in_time']
                out_datetime = attn_raw_data['out_time']
                daily_attn = ProcessAttendanceDaily.objects.get(attn_date=attn_raw_data['attn_date'],staff=attn_raw_data['staff'],is_active=True,status=True)
                if daily_attn:
                    shift_start_time = daily_attn.shift.start_time
                    in_time = in_datetime.time()
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
                    daily_attn.attn_type = att_type
                    daily_attn.save()
            return Response('okay')
        except:
            return Response('Something Worng!!!!!!!!!!!')

    def create(self, request, *args, **kwargs):
        data=request.data
        attn_date = data['proc_date']
        attn_date = datetime.strptime(attn_date, '%Y-%m-%d')
        try:
            attn_raw_datas = AttendanceDailyRaw.objects.filter(attn_date=attn_date,staff__isnull=False,is_active=True, status=True).values('staff', 'attn_date').annotate(
                                        in_time=Coalesce(Min('trnsc_time'), F('attn_date')),
                                        out_time=Coalesce(Max('trnsc_time'), F('attn_date'))
                                    )
            for attn_raw_data in attn_raw_datas:
                in_datetime = attn_raw_data['in_time']
                out_datetime = attn_raw_data['out_time']
                daily_attn = ProcessAttendanceDaily.objects.get(attn_date=attn_raw_data['attn_date'],staff=attn_raw_data['staff'],is_active=True,status=True)
                if daily_attn:
                    shift_start_time = daily_attn.shift.start_time
                    in_time = in_datetime.time()
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
                    daily_attn.attn_type = att_type
                    daily_attn.save()
            return Response('okay')
        except:
            return Response('Something Worng!!!!!!!!!!!')

class staffLeaveTransactionCreate(generics.CreateAPIView):
    serializer_class = StaffLeaveTransactionCreateSerializer
    permission_classes = [permissions.IsAuthenticated]  # Requires a valid JWT token for access
    pagination_class = CustomPagination

    def create(self, request, *args, **kwargs):
        '''Check user has permission to Create start'''
        permission_check = check_permission(self.request.user.id, 'Apply Leave', 'create')
        if not permission_check:
            return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to Create End'''
        
        serializer = self.get_serializer(data=request.data)
        try:
            if serializer.is_valid():
                institution_data = serializer.validated_data.get('institution')
                branch_data = serializer.validated_data.get('branch')
                # If data is provided, use it; otherwise, use the values from the request user
                institution = institution_data if institution_data is not None else self.request.user.institution
                branch = branch_data if branch_data is not None else self.request.user.branch
                apply_by = serializer.validated_data.get('apply_by')
                leave_type = serializer.validated_data.get('leave_type')
                responsible = serializer.validated_data.get('responsible')
                start_date = serializer.validated_data.get('start_date')
                end_date = serializer.validated_data.get('end_date')
                if start_date == end_date:
                    day_name = start_date.strftime('%A').lower()
                    if(day_name=='friday'):
                        return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message="You Can't create leave on Weekend", data=None)
                if not apply_by:
                    username = self.request.user
                    apply_by = Staff.objects.get(staff_id=username,status=True)
                if apply_by==responsible:
                    return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message="আপনি নিজেকে নিজে দায়িত্বশীল ব্যক্তি হিসাবে সেট করতে পারবেন না।", data=None)
                leave_remain_days = 0
                staff_leave_counnt = StaffLeave.objects.filter(staff=apply_by,leave_type=leave_type,is_active=True,status=True,institution=institution, branch=branch).count()
                if staff_leave_counnt == 0:
                    return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message="Leave is not assign", data=None)
                for leave_status in StaffLeave.objects.filter(staff=apply_by,leave_type=leave_type,is_active=True,status=True,institution=institution, branch=branch).order_by('id'):
                    staff_leave_id = leave_status.id
                    leave_day = leave_status.leave_days
                    proces_day = leave_status.process_days
                    taken_day = leave_status.taken_days
                    leave_remain_days = leave_day - (taken_day+proces_day)
                start_date = serializer.validated_data.get('start_date')
                end_date = serializer.validated_data.get('end_date')
                duration = 1 + (end_date - start_date).days
                total_proces_day = proces_day + duration
                leave_trns_count = StaffLeaveTransaction.objects.filter(Q(is_active=True) ,Q(status=True),Q(apply_by=apply_by),Q(institution=institution), Q(branch=branch),Q(start_date__range=(start_date, end_date)) | Q(end_date__range=(start_date, end_date))).count()
                if leave_trns_count > 0:
                    return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message="Leave Already Applied", data=None)
                if duration > leave_remain_days:
                    return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message="দুঃখিত!! আপনি ইতিমধ্যে সব ছুটি গ্রহণ করেছেন", data=None)
                if start_date > end_date:
                    return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message="End date must be greater than or equal to start date", data=None)
                # version = serializer.validated_data.get('version')
                submit_status = Setup.objects.get(status=True,parent__type='APPROVAL_STATUS',type='SUBMITTED',institution=institution,branch=branch)
                instance = serializer.save(apply_by=apply_by,app_status=submit_status,institution=institution, branch=branch)
                queryset = StaffLeave.objects.filter(staff=apply_by,leave_type=leave_type,is_active=True,status=True,institution=institution, branch=branch)
                leave_date = get_object_or_404(queryset, pk=staff_leave_id)
                data = {
                    "process_days" : total_proces_day
                }
                leave_serializer = StaffLeaveCreateSerializer(leave_date,partial=True,data=data)
                if leave_serializer.is_valid():
                    leave_serializer.save()
                app_groups = Setup.objects.filter(status=True,parent__type='STAFF_LEAVE_APP_HIR',institution=institution,branch=branch)
                for app_group in app_groups:
                    if(app_group.type=='SUBMITTED'):
                        StaffLeaveAppHistory.objects.create(app_status=submit_status,approve_date=datetime.now(),leave_trns=instance,approve_by=apply_by,approve_group=app_group,institution=institution, branch=branch)
                    else:
                        StaffLeaveAppHistory.objects.create(approve_by=responsible,leave_trns=instance,approve_group=app_group,institution=institution, branch=branch)
                    # Customize the response data
                return CustomResponse(code=status.HTTP_200_OK, message="Leave created successfully", data=StaffLeaveTransactionViewSerializer(instance).data)
                # return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message=f"Version {version} already exits", data=serializer.errors)
            # If the serializer is not valid, return an error response
            return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message="Validation error", data=serializer.errors)
        except Exception as e:
            # Handle other exceptions
            return CustomResponse(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="An error occurred during the Create", data=str(e))

class staffLeaveTransactionUpdate(generics.RetrieveUpdateAPIView):
    queryset = StaffLeaveTransaction.objects.all()
    serializer_class = StaffLeaveTransactionCreateSerializer
    permission_classes = [permissions.IsAuthenticated]  # Requires a valid JWT token for access
    
    def retrieve(self, request, *args, **kwargs):
        '''Check user has permission to retrive start'''
        permission_check = check_permission(self.request.user.id, 'Apply Leave', 'view')
        if not permission_check:
            return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to retrive End'''
        
        instance = self.get_object()
        # Customize the response format for retrieving a single instance
        return CustomResponse(code=status.HTTP_200_OK, message="Success", data=StaffLeaveTransactionViewSerializer(instance).data)

    def update(self, request, *args, **kwargs):
        '''Check user has permission to update start'''
        permission_check = check_permission(self.request.user.id, 'Apply Leave', 'update')
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
                institution = institution_data if institution_data is not None else self.request.user.institution
                branch = branch_data if branch_data is not None else self.request.user.branch
                start_date = serializer.validated_data.get('start_date')
                end_date = serializer.validated_data.get('end_date')
                leave_type = serializer.validated_data.get('leave_type')
                apply_by = serializer.validated_data.get('apply_by')
                responsible = serializer.validated_data.get('responsible')
                if start_date == end_date:
                    day_name = start_date.strftime('%A').lower()
                    if(day_name=='friday'):
                        return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message="You Can't create leave on Weekend", data=None)
                if not apply_by:
                    username = self.request.user
                    apply_by = Staff.objects.get(staff_id=username,status=True)
                if apply_by==responsible:
                    return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message="আপনি নিজেকে নিজে দায়িত্বশীল ব্যক্তি হিসাবে সেট করতে পারবেন না।", data=None)
                if not apply_by:
                    username = self.request.user
                    apply_by = Staff.objects.get(staff_id=username,status=True)
                # Check applied user is same or not
                if (apply_by != instance.apply_by):
                    return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message="Sorry! You can't change leave person.", data=None)
                # Check Start date < end Date
                if start_date > end_date:
                    return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message="End date must be greater than or equal to start date", data=None)
                # start date , end date and leave type is same
                if (start_date==instance.start_date and end_date==instance.end_date and leave_type == instance.leave_type):
                    instance = serializer.save()
                    return CustomResponse(code=status.HTTP_200_OK, message="Leave Updated successfully", data=StaffLeaveTransactionViewSerializer(instance).data)
                # Check if leave was applied during those date
                leave_trns_count = StaffLeaveTransaction.objects.filter(Q(is_active=True),(~Q(id=instance.id)),Q(status=True),Q(apply_by=apply_by),Q(institution=institution), Q(branch=branch),Q(start_date__range=(start_date, end_date)) | Q(end_date__range=(start_date, end_date))).count()
                if leave_trns_count > 0:
                    return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message="Leave Already Applied", data=None)
                # if (start_date!=instance.start_date or end_date!=instance.end_date or leave_type != instance.leave_type):

                if ((start_date!=instance.start_date or end_date!=instance.end_date) and leave_type == instance.leave_type):
                    duration = 1 + (end_date - start_date).days
                    old_duration = 1 + (instance.end_date - instance.start_date).days
                    staff_leave = StaffLeave.objects.filter(staff=apply_by,leave_type=leave_type,is_active=True,status=True,institution=institution, branch=branch).order_by('-id').last()
                    process_days = staff_leave.process_days
                    queryset = StaffLeave.objects.filter(staff=apply_by,leave_type=leave_type,is_active=True,status=True,institution=institution, branch=branch)
                    leave_date = get_object_or_404(queryset, pk=staff_leave.id)
                    duration_diff = (duration-old_duration)
                    if duration_diff > 0:
                        leave_remain_days = staff_leave.leave_days - (staff_leave.taken_days+(staff_leave.process_days-old_duration))
                        if duration > leave_remain_days:
                            return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message="দুঃখিত!! আপনি ইতিমধ্যে সব ছুটি গ্রহণ করেছেন", data=None)
                    new_duration = process_days + duration_diff
                    instance = serializer.save()
                    data = {
                       "process_days" : new_duration
                    }
                    leave_serializer = StaffLeaveCreateSerializer(leave_date,partial=True,data=data)
                    if leave_serializer.is_valid():
                        leave_serializer.save()
                    return CustomResponse(code=status.HTTP_200_OK, message="Leave Updated successfully", data=StaffLeaveTransactionViewSerializer(instance).data)
                if (leave_type != instance.leave_type):
                    staff_leave_old = StaffLeave.objects.filter(staff=apply_by,leave_type=instance.leave_type,is_active=True,status=True,institution=institution, branch=branch).order_by('-id').last()
                    staff_leave = StaffLeave.objects.filter(staff=apply_by,leave_type=leave_type,is_active=True,status=True,institution=institution, branch=branch).order_by('-id').last()
                    process_days_old = staff_leave_old.process_days
                    duration = 1 + (end_date - start_date).days
                    leave_remain_days = staff_leave.leave_days - (staff_leave.taken_days+(staff_leave.process_days))
                    if duration > leave_remain_days:
                        return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message="দুঃখিত!! আপনি ইতিমধ্যে সব ছুটি গ্রহণ করেছেন", data=None)
                    old_duration = 1 + (instance.end_date - instance.start_date).days
                    queryset_old = StaffLeave.objects.filter(staff=apply_by,leave_type=instance.leave_type,is_active=True,status=True,institution=institution, branch=branch)
                    leave_date_old = get_object_or_404(queryset_old, pk=staff_leave_old.id)
                    new_duration = (process_days_old-old_duration)
                    data_old = {
                        "process_days" : new_duration
                        }
                    leave_serializer_old = StaffLeaveCreateSerializer(leave_date_old,partial=True,data=data_old)
                    if leave_serializer_old.is_valid():
                        leave_serializer_old.save()

                    duration = 1 + (end_date - start_date).days
                    old_duration = 1 + (instance.end_date - instance.start_date).days
                    
                    process_days = staff_leave.process_days
                    queryset = StaffLeave.objects.filter(staff=apply_by,leave_type=leave_type,is_active=True,status=True,institution=institution, branch=branch)
                    leave_date = get_object_or_404(queryset, pk=staff_leave.id)
                    duration_diff = (duration-old_duration)
                    new_duration = process_days + duration
                    
                    
                    data = {
                       "process_days" : new_duration
                    }
                    leave_serializer = StaffLeaveCreateSerializer(leave_date,partial=True,data=data)
                    if leave_serializer.is_valid():
                        leave_serializer.save()
                    
                    instance = serializer.save()
                    return CustomResponse(code=status.HTTP_200_OK, message="Leave Updated successfully", data=StaffLeaveTransactionViewSerializer(instance).data)
                
            else:
                # Handle validation errors
                return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message="Validation error", data=serializer.errors)
        except Exception as e:
            # Handle other exceptions
            return CustomResponse(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="An error occurred during the update", data=str(e))

class staffLeaveTransactionList(generics.RetrieveAPIView):
    queryset = StaffLeaveTransaction.objects.all()
    serializer_class = StaffLeaveTransactionListSerializer
    permission_classes = [permissions.IsAuthenticated]  # Requires a valid JWT token for access
    
    def retrieve(self, request, *args, **kwargs):
        '''Check user has permission to retrive start'''
        permission_check = check_permission(self.request.user.id, 'Apply Leave', 'view')
        if not permission_check:
            return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to retrive End'''
        
        instance = self.get_object()
        # Customize the response format for retrieving a single instance
        return CustomResponse(code=status.HTTP_200_OK, message="Success", data=StaffLeaveTransactionListSerializer(instance).data)

class staffLeaveStatusList(generics.ListAPIView):
    serializer_class = StaffLeaveViewSerialier
    permission_classes = [permissions.IsAuthenticated]  # Requires a valid JWT token for access
    pagination_class = CustomPagination

    def get_queryset(self):
        # Get the role ID from the URL parameter
        institution_id = self.request.user.institution
        branch_id = self.request.user.branch
        start_date = datetime(datetime.now().year,1,1)
        end_date = datetime(datetime.now().year,12,31)
        staff_id = int(self.kwargs['staff_id'])
        queryset = StaffLeave.objects.filter(staff__id=staff_id,status=True,start_date__range=[start_date, end_date],end_date__range=[start_date, end_date],institution=institution_id,branch=branch_id)
        try:
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

class StaffLeaveTrnsAlllLst(generics.ListAPIView):
    serializer_class = StaffLeaveTransactionViewSerializer
    permission_classes = [permissions.IsAuthenticated]  # Requires a valid JWT token for access
    pagination_class = CustomPagination

    def get_queryset(self):
        # Get the role ID from the URL parameter
        institution_id = self.request.user.institution
        branch_id = self.request.user.branch
        queryset = StaffLeaveTransaction.objects.filter(status=True,institution=institution_id,branch=branch_id)
        try:
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

class StaffLeaveTrnsPersonallLst(generics.ListAPIView):
    serializer_class = StaffLeaveTransactionViewSerializer
    permission_classes = [permissions.IsAuthenticated]  # Requires a valid JWT token for access
    pagination_class = CustomPagination

    def get_queryset(self):
        # Get the role ID from the URL parameter
        institution_id = self.request.user.institution
        branch_id = self.request.user.branch
        staff_id = Staff.objects.get(status=True,user=self.request.user.id)
        print(staff_id)
        queryset = StaffLeaveTransaction.objects.filter(status=True,institution=institution_id,branch=branch_id,apply_by=staff_id)
        try:
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

class StaffLeaveTrnslLst(generics.ListAPIView):
    serializer_class = StaffLeaveTransactionViewSerializer
    permission_classes = [permissions.IsAuthenticated]  # Requires a valid JWT token for access
    pagination_class = CustomPagination

    def get_queryset(self):
        # Get the role ID from the URL parameter
        institution_id = self.request.user.institution
        branch_id = self.request.user.branch
        staff_id = int(self.kwargs['staff_id'])
        queryset = StaffLeaveTransaction.objects.filter(apply_by__id=staff_id,status=True,institution=institution_id,branch=branch_id)
        try:
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

class StaffLeaveList(generics.ListAPIView):
    serializer_class = StaffLeaveViewSerialier
    permission_classes = [permissions.IsAuthenticated]  # Requires a valid JWT token for access
    pagination_class = CustomPagination

    def get_queryset(self):
        username = self.request.user
        institution = self.request.user.institution
        branch = self.request.user.branch
        staff_id = self.request.query_params.get('staff_id')
        if staff_id:
            queryset = StaffLeave.objects.filter(staff=staff_id,status=True,is_active=True,institution=institution,branch=branch)
        else:
            staff_id = Staff.objects.get(staff_id=username,status=True)
            queryset = StaffLeave.objects.filter(staff=staff_id,status=True,is_active=True,institution=institution,branch=branch)
        return queryset


    def list(self,request,*args, **kwargs):
        '''Check user has permission to View start'''
        # permission_check = check_permission(self.request.user.id, 'Staff Shift', 'view')
        # if not permission_check:
        #     return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to View end'''
        try:
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
        except:
            response_data = {
                    "code": 400,
                    "message": "Bad Request",
                    "data": None,
                }

        return Response(response_data)

class StaffLeaveTypeList(generics.ListAPIView):
    serializer_class = StaffLeaveListSerialier
    # Requires a valid JWT token for access
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        institution_id = self.request.user.institution
        branch_id = self.request.user.branch
        staff_id = Staff.objects.get(status=True,user=self.request.user.id)
        queryset = StaffLeave.objects.filter(status=True,is_active=True,staff=staff_id,leave_days__gt = F('taken_days')+F('process_days')).order_by('-id')
        try:
            # users = Authentication.objects.get(id=user_id)
            if institution_id and branch_id:
                queryset = queryset.filter(institution=institution_id, branch=branch_id, status=True).order_by('-id')
            elif branch_id:
                queryset = queryset.filter(branch=branch_id, status=True).order_by('-id')
            elif institution_id:
                queryset = queryset.filter(institution=institution_id, status=True).order_by('-id')
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

class StaffPunchData(generics.ListAPIView):
    def list(self, request, *args, **kwargs):
        url = f"http://192.168.117.152:5002/waltonagro/attn_data"
        attn_date = self.request.query_params.get('attn_date')
        if attn_date:
            pass
        else:
            attn_date = datetime.now().date()
        payload = ""
        headers = {}
        response = requests.request("GET",url,headers=headers,data=payload)
        json_data = response.json()
        attn_data = json_data['attendance_data']
        punch_data = {}
        for i in attn_data:
            if attn_date == datetime.strptime(i['punch_time'], '%Y-%m-%d %H:%M:%S').date():
                attn_count = AttendanceDailyRaw.objects.filter(staff_code=i['user_id'],trnsc_time=datetime.strptime(i['punch_time'], '%Y-%m-%d %H:%M:%S')).count()
                if attn_count == 0:
                    punch_data['device_ip'] = i['device_ip']
                    punch_data['attn_date'] = datetime.strptime(i['punch_time'], '%Y-%m-%d %H:%M:%S').date()
                    punch_data['trnsc_time'] = datetime.strptime(i['punch_time'], '%Y-%m-%d %H:%M:%S')
                    punch_data['device_name'] = i['device_name']
                    punch_data['device_serial'] = i['device_serial']
                    punch_data['email'] = i['email']
                    punch_data['mobile'] = i['mobile']
                    punch_data['staff_code'] = i['user_id']
                    punch_data['src_type'] = 'device'
                    try:
                        staff_info = Staff.objects.get(staff_id=i['user_id'],status=True)
                        punch_data['staff'] = staff_info
                        punch_data['institution'] = staff_info.institution
                        punch_data['branch'] = staff_info.branch
                    except:
                        punch_data['staff'] = None
                        punch_data['institution'] = None
                        punch_data['branch'] = None
                    punch_data['username'] = i['username']
                    p = AttendanceDailyRaw.objects.create(**punch_data)
                else:
                    pass
        return Response(punch_data)     

class StaffAttendanceSummeryProcess(generics.CreateAPIView):
    serializer_class = ProcessStaffAttendanceMstCreateSerializer
    permission_classes = [permissions.IsAuthenticated]  # Requires a valid JWT token for access
    pagination_class = CustomPagination

    def create(self, request, *args, **kwargs):
        institution_id = self.request.user.institution
        branch_id = self.request.user.branch
        from_date = request.data.get('from_date')
        from_date = datetime.strptime(from_date, '%Y-%m-%d')
        to_date = request.data.get('to_date')
        to_date = datetime.strptime(to_date, '%Y-%m-%d')
        day_diff = (to_date - from_date).days + 1
        if day_diff <= 0:
            return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message="From date is less than To date", data=None)
        staff_infos = Staff.objects.filter(status=True,institution=institution_id,branch=branch_id)
        for staff_info in staff_infos:
            process_count = ProcessStaffAttendanceMst.objects.filter(Q(staff=staff_info),Q(status=True),Q(from_date__range=(from_date, to_date)) | Q(to_date__range=(from_date, to_date))).count()
            min_duration = timedelta(minutes=10)
            attn_late_infos = ProcessAttendanceDaily.objects.filter(status=True,is_active=True,
                                                                      staff=staff_info,attn_date__range=(from_date, to_date),
                                                                    #   late_by_min__gte=min_duration,
                                                                     late_by_min__gt = min_duration,
                                                                      attn_type__name__iexact = 'late'
                                                                      )
            # Calculate the sum of late_by_min
            total_late_by_min = attn_late_infos.aggregate(total_late=Sum('late_by_min'))['total_late']
            for attn_late_info in attn_late_infos:
                print((attn_late_info.late_by_min/60).total_seconds())
            print(staff_info,process_count)
            if process_count == 0:
                staff_payroll = StaffPayroll.objects.filter(Q(status=True),
                                                            Q(is_active=True),
                                                            Q(staff=staff_info),
                                                            Q(start_date__lte=from_date),
                                                            Q(end_date__isnull=True) | Q(end_date__gte=to_date)
                                                            ).order_by('-start_date').last()
                proc_attn_mst = {}
                attn_leave_types = ['al','cl','ml']
                attn_type_queries = Q()
                for attn_type in attn_leave_types:
                    attn_type_queries |= Q(attn_type__name__iexact=attn_type)

                if staff_payroll:
                    staff_payroll_id = staff_payroll
                    staff_type = staff_payroll.contract_type.name.lower()
                    staff_gross = staff_payroll.gross
                else:
                    staff_type = None
                    staff_payroll_id = None
                    staff_gross = 0
                total_days = ProcessAttendanceDaily.objects.filter(status=True,is_active=True,
                                                                   staff=staff_info,attn_date__range=(from_date, to_date)
                                                                   ).count()
                total_present = ProcessAttendanceDaily.objects.filter(status=True,is_active=True,
                                                                      staff=staff_info,attn_date__range=(from_date, to_date),
                                                                      attn_type__name__iexact = 'present'
                                                                      ).count()
                total_absent = ProcessAttendanceDaily.objects.filter(status=True,is_active=True,
                                                                      staff=staff_info,attn_date__range=(from_date, to_date),
                                                                      attn_type__name__iexact = 'absent'
                                                                      ).count()
                total_weekend = ProcessAttendanceDaily.objects.filter(status=True,is_active=True,
                                                                      staff=staff_info,attn_date__range=(from_date, to_date),
                                                                      attn_type__name__iexact = 'weekend'
                                                                      ).count()
                total_holiday = ProcessAttendanceDaily.objects.filter(status=True,is_active=True,
                                                                      staff=staff_info,attn_date__range=(from_date, to_date),
                                                                      attn_type__name__iexact = 'holiday'
                                                                      ).count()
                total_late = ProcessAttendanceDaily.objects.filter(status=True,is_active=True,
                                                                      staff=staff_info,attn_date__range=(from_date, to_date),
                                                                      attn_type__name__iexact = 'late'
                                                                      ).count()
                total_early_gone = ProcessAttendanceDaily.objects.filter(status=True,is_active=True,
                                                                      staff=staff_info,attn_date__range=(from_date, to_date),
                                                                      attn_type__name__iexact = 'early gone'
                                                                      ).count()
                total_on_tour = ProcessAttendanceDaily.objects.filter(status=True,is_active=True,
                                                                      staff=staff_info,attn_date__range=(from_date, to_date),
                                                                      attn_type__name__iexact = 'on tour'
                                                                      ).count()
                total_leave = ProcessAttendanceDaily.objects.filter(Q(status=True),
                                                                        Q(is_active=True),
                                                                        Q(staff=staff_info),
                                                                        Q(attn_date__range=(from_date, to_date)),
                                                                        attn_type_queries
                                                                      ).count()
                if staff_type == 'daily labor':
                    payable_days = total_present + total_late + total_early_gone + total_on_tour
                    staff_main_grouss = payable_days * staff_gross
                else:
                    payable_days = total_present + total_late + total_early_gone + total_holiday + total_weekend
                    staff_main_grouss = staff_gross
                # print(total_days,staff_info,payable_days,total_present,total_absent,total_weekend,total_holiday,total_late,staff_main_grouss,total_leave,total_on_tour)

                proc_attn_mst['staff'] = staff_info
                proc_attn_mst['staff_code'] = staff_info.staff_id
                proc_attn_mst['from_date'] = from_date
                proc_attn_mst['to_date'] = to_date
                proc_attn_mst['staff_payroll'] = staff_payroll_id
                proc_attn_mst['present_day'] = total_present
                proc_attn_mst['absent_day'] = total_absent
                proc_attn_mst['late_day'] = total_late
                proc_attn_mst['early_gone_day'] = total_early_gone
                proc_attn_mst['tour_day'] = total_on_tour
                proc_attn_mst['tot_payble_day'] = payable_days
                proc_attn_mst['weekend_day'] = total_weekend
                proc_attn_mst['holiday_day'] = total_holiday
                proc_attn_mst['actual_gross'] = staff_main_grouss
                proc_attn_mst['institution'] = staff_info.institution
                proc_attn_mst['branch'] = staff_info.branch
                p = ProcessStaffAttendanceMst.objects.create(**proc_attn_mst)

                # print(proc_attn_mst)


        return CustomResponse(code=status.HTTP_200_OK, message="Process Done", data=None)

class StaffStatusCreate(generics.ListCreateAPIView):
    serializer_class = StaffStatusTransactionViewSerializer
    permission_classes = [permissions.IsAuthenticated]  # Requires a valid JWT token for access
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = StaffStatusTransaction.objects.filter(status=True).order_by('-id')
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
        # permission_check = check_permission(self.request.user.id, 'Department', 'view')
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
    
    def create(self, request, *args, **kwargs):
        '''Check user has permission to Create start'''
        # permission_check = check_permission(self.request.user.id, 'Department', 'create')
        # if not permission_check:
        #     return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to Create End'''
        
        serializer_class = StaffStatusTransactionCreateSerializer
        serializer = serializer_class(data=request.data)
        try:
            if serializer.is_valid():
                institution_data = serializer.validated_data.get('institution')
                branch_data = serializer.validated_data.get('branch')
                # If data is provided, use it; otherwise, use the values from the request user
                institution = institution_data if institution_data is not None else self.request.user.institution
                branch = branch_data if branch_data is not None else self.request.user.branch
                instance = serializer.save(institution=institution,branch=branch)
                # Customize the response data
                return CustomResponse(code=status.HTTP_200_OK, message="Staff Status created successfully", data=StaffStatusTransactionViewSerializer(instance).data)
            # If the serializer is not valid, return an error response
            return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message="Validation error", data=serializer.errors)
        except Exception as e:
            # Handle other exceptions
            return CustomResponse(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="An error occurred during the Create", data=str(e))

class StaffLeaveHistoryUpdate(generics.RetrieveUpdateAPIView):
    queryset = StaffLeaveAppHistory.objects.all()
    serializer_class = StaffLeaveAppHistoryCreateSerializer
    permission_classes = [permissions.IsAuthenticated]  # Requires a valid JWT token for access
    
    def retrieve(self, request, *args, **kwargs):
        '''Check user has permission to View start'''
        # permission_check = check_permission(self.request.user.id, 'Class Subject', 'view')
        # if not permission_check:
        #     return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to View end'''
        instance = self.get_object()
        # Customize the response format for retrieving a single instance
        return CustomResponse(code=status.HTTP_200_OK, message="Success", data=StaffLeaveAppHistoryViewSerializer(instance).data)

    def update(self, request, *args, **kwargs):
        '''Check user has permission to View start'''
        # permission_check = check_permission(self.request.user.id, 'Class Subject', 'update')
        # if not permission_check:
        #     return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to View end'''
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer_class = StaffLeaveAppHistoryCreateSerializer
        serializer = serializer_class(instance, data=request.data, partial=partial)
        
        try:
            if serializer.is_valid():
                if instance.leave_trns.app_status.type == 'APPROVED':
                    return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message="Sorry, Staff Leave Already Approved!!!", data=None)
                if instance.leave_trns.app_status.type == 'DENY':
                    return CustomResponse(code=status.HTTP_403_FORBIDDEN, message="Sorry, Staff Leave Already Deny!!!", data=None)
                # Perform any custom update logic here if needed
                instance = serializer.save()
                # Customize the response format for successful update
                return CustomResponse(code=status.HTTP_200_OK, message="Staff Leave Approved successfully", data=StaffLeaveAppHistoryViewSerializer(instance).data)
            else:
                # Handle validation errors
                return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message="Validation error", data=serializer.errors)
        except Exception as e:
            # Handle other exceptions
            return CustomResponse(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="An error occurred during the update", data=str(e))

class StaffDailyAttnList(generics.ListAPIView):
    serializer_class = ProcessAttendanceViewDailySerializer
    permission_classes = [permissions.IsAuthenticated]  # Requires a valid JWT token for access
    pagination_class = CustomPagination

    def get_queryset(self):
        username = self.request.user
        user_info = self.request.user.id
        model_name = self.request.user.model_name
        institution = self.request.user.institution
        branch = self.request.user.branch
        from_date = self.request.query_params.get('from_date')
        to_date = self.request.query_params.get('to_date')
        print(from_date,to_date)
        # staff_id = self.request.query_params.get('staff_id')
        if from_date and to_date:
            queryset = ProcessAttendanceDaily.objects.filter(attn_date__range=(from_date, to_date),staff__user=user_info,status=True,is_active=True,institution=institution,branch=branch).order_by('attn_date')
        else:
            queryset = ProcessAttendanceDaily.objects.filter(staff__user=user_info,status=True,is_active=True,institution=institution,branch=branch).order_by('-attn_date')[:5]
        return queryset


    def list(self,request,*args, **kwargs):
        '''Check user has permission to View start'''
        # permission_check = check_permission(self.request.user.id, 'Staff Shift', 'view')
        # if not permission_check:
        #     return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to View end'''
        try:
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
        except:
            response_data = {
                    "code": 400,
                    "message": "Bad Request",
                    "data": None,
                }

        return Response(response_data)

class StaffPayrollProcess(generics.ListAPIView):
    # serializer_class = ProcessStaffSalaryTableCreateSerializer
    permission_classes = [permissions.IsAuthenticated]  # Requires a valid JWT token for access
    pagination_class = CustomPagination

    # def get_queryset(self):
    #     institution_id = self.request.user.institution
    #     branch_id = self.request.user.branch
    #     staff_id = self.request.query_params.get('staff_id')
        
        

    def list(self,request,*args, **kwargs):
        institution_id = self.request.user.institution
        branch_id = self.request.user.branch
        from_date = self.request.query_params.get('from_date')
        if from_date:
            from_date = datetime.strptime(from_date,'%Y-%m-%d').date()
        to_date = self.request.query_params.get('to_date')
        if to_date:
            to_date = datetime.strptime(to_date,'%Y-%m-%d').date()

        if from_date > to_date:
            return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message=f"From date {from_date} is less than To date {to_date}", data=None)
        staff_id = self.request.query_params.get('staff_id')
        if staff_id:
            staffs_data = Staff.objects.filter(status=True,institution=institution_id,branch=branch_id,staff_id=staff_id)
        else:
            staffs_data = Staff.objects.filter(status=True,institution=institution_id,branch=branch_id)
        for staff_data in staffs_data:
            print(staff_data.staff_id)
            process_count = ProcessStaffSalaryTable.objects.filter(status=True,is_active=True,staff_no=staff_data.
                                                                   staff_id,from_date__range=(from_date, to_date),to_date__range=(from_date, to_date)).count()
            print(process_count)
            if process_count == 0:
                print(staff_data.staff_status.name.lower())
                payroll_proc_data = {}
                payroll_proc_data['from_date'] = from_date
                payroll_proc_data['to_date'] = to_date
                payroll_proc_data['staff'] = staff_data
                payroll_proc_data['institution'] = staff_data.institution
                payroll_proc_data['branch'] = staff_data.branch
                if staff_data.staff_status.name.lower()!='active':
                    payroll_proc_data['is_hold']=True
                p = ProcessStaffSalaryTable.objects.create(**payroll_proc_data)
                print(payroll_proc_data)

        return CustomResponse(code=status.HTTP_200_OK, message=f"Process Done....", data=None)
