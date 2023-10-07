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
# Create your views here.
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