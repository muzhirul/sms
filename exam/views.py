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
'''
For Grade
'''
class GradeCreateList(generics.ListCreateAPIView):
    serializer_class = GradeSerializer
    permission_classes = [permissions.IsAuthenticated]  # Requires a valid JWT token for access
    pagination_class = CustomPagination
    
    def get_queryset(self):
        queryset = Grade.objects.filter(status=True).order_by('sl_no')
        try:
            institution_id = self.request.user.institution
            branch_id = self.request.user.branch
            # users = Authentication.objects.get(id=user_id)
            if institution_id and branch_id:
                queryset = queryset.filter(institution=institution_id, branch=branch_id,status=True).order_by('sl_no')
            elif branch_id:
                queryset = queryset.filter(branch=branch_id,status=True).order_by('sl_no')
            elif institution_id:
                queryset = queryset.filter(institution=institution_id,status=True).order_by('sl_no')
            else:
                queryset            
        except:
            pass
        return queryset
        
    def list(self,request,*args, **kwargs):
        '''Check user has permission to View start'''
        permission_check = check_permission(self.request.user.id, 'Grade', 'view')
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
        permission_check = check_permission(self.request.user.id, 'Grade', 'create')
        if not permission_check:
            return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to View end'''
        serializer = self.get_serializer(data=request.data)
        try:
            if serializer.is_valid():
                institution_data = serializer.validated_data.get('institution')
                branch_data = serializer.validated_data.get('branch')
                # If data is provided, use it; otherwise, use the values from the request user
                institution = institution_data if institution_data is not None else self.request.user.institution
                branch = branch_data if branch_data is not None else self.request.user.branch

                instance = serializer.save(institution=institution, branch=branch)
                # Customize the response data
                return CustomResponse(code=status.HTTP_200_OK, message="Grade created successfully", data=GradeSerializer(instance).data)
            # If the serializer is not valid, return an error response
            return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message="Validation error", data=serializer.errors)
        except Exception as e:
            # Handle other exceptions
            return CustomResponse(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="An error occurred during the Create", data=str(e))

class GradeDetailUpdate(generics.RetrieveUpdateAPIView):
    queryset = Grade.objects.filter(status=True)
    serializer_class = GradeSerializer
    permission_classes = [permissions.IsAuthenticated]  # Requires a valid JWT token for access
    
    def retrieve(self, request, *args, **kwargs):
        '''Check user has permission to retrive start'''
        permission_check = check_permission(self.request.user.id, 'Grade', 'view')
        if not permission_check:
            return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        try:
            '''Check user has permission to retrive End'''
            instance = self.get_object()
            # Customize the response format for retrieving a single instance
            return CustomResponse(code=status.HTTP_200_OK, message="Success", data=GradeSerializer(instance).data)
        except:
            return CustomResponse(code=status.HTTP_404_NOT_FOUND, message="Not Found", data=None)

    def update(self, request, *args, **kwargs):
        '''Check user has permission to update start'''
        permission_check = check_permission(self.request.user.id, 'Grade', 'update')
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
                point = serializer.validated_data.get('point')
                start_mark = serializer.validated_data.get('start_mark')
                end_mark = serializer.validated_data.get('end_mark')
                institution = institution_data if institution_data is not None else self.request.user.institution
                branch = branch_data if branch_data is not None else self.request.user.branch
                routine_count = Grade.objects.filter(name=name,point=point,start_mark=start_mark,end_mark=end_mark,institution=institution,branch=branch,status=True).count()
                if (routine_count==0):
                    # Perform any custom update logic here if needed
                    instance = serializer.save()
                    # Customize the response format for successful update
                    return CustomResponse(code=status.HTTP_200_OK, message="Grade updated successfully", data=GradeSerializer(instance).data)
                return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message=f"This Grade already exits", data=serializer.errors)
            else:
                # Handle validation errors
                return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message="Validation error", data=serializer.errors)
        except Exception as e:
            # Handle other exceptions
            return CustomResponse(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="An error occurred during the update", data=str(e))
        
class GradeDelete(generics.UpdateAPIView):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer
    permission_classes = [permissions.IsAuthenticated]  # Requires a valid JWT token for access
    
    def partial_update(self, request, *args, **kwargs):
        '''Check user has permission to Delete start'''
        permission_check = check_permission(self.request.user.id, 'Grade', 'delete')
        if not permission_check:
            return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to Delete End'''
        try:
            instance = self.get_object()
            if not instance.status:
                return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message=f"Grade already Deleted", data=None)
            # Update the "status" field to False
            instance.status = False
            instance.save()
            # Customize the response format for successful update
            return CustomResponse(code=status.HTTP_200_OK, message=f"Grade Delete successfully", data=None)
        except:
            return CustomResponse(code=status.HTTP_404_NOT_FOUND, message="Not Found", data=None)

'''
For Exam Name
'''
class ExamNameCreateList(generics.ListCreateAPIView):
    serializer_class = ExamNameViewSerializer
    permission_classes = [permissions.IsAuthenticated]  # Requires a valid JWT token for access
    pagination_class = CustomPagination
    
    def get_queryset(self):
        queryset = ExamName.objects.filter(status=True).order_by('sl_no')
        try:
            institution_id = self.request.user.institution
            branch_id = self.request.user.branch
            # users = Authentication.objects.get(id=user_id)
            if institution_id and branch_id:
                queryset = queryset.filter(institution=institution_id, branch=branch_id,status=True).order_by('sl_no')
            elif branch_id:
                queryset = queryset.filter(branch=branch_id,status=True).order_by('sl_no')
            elif institution_id:
                queryset = queryset.filter(institution=institution_id,status=True).order_by('sl_no')
            else:
                queryset            
        except:
            pass
        return queryset
        
    def list(self,request,*args, **kwargs):
        '''Check user has permission to View start'''
        permission_check = check_permission(self.request.user.id, 'Exam Name', 'view')
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
        permission_check = check_permission(self.request.user.id, 'Exam Name', 'create')
        if not permission_check:
            return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to View end'''
        serializer_class = ExamNameCreateSerializer
        serializer = serializer_class(data=request.data)
        try:
            if serializer.is_valid():
                institution_data = serializer.validated_data.get('institution')
                branch_data = serializer.validated_data.get('branch')
                # If data is provided, use it; otherwise, use the values from the request user
                institution = institution_data if institution_data is not None else self.request.user.institution
                branch = branch_data if branch_data is not None else self.request.user.branch

                instance = serializer.save(institution=institution, branch=branch)
                # Customize the response data
                return CustomResponse(code=status.HTTP_200_OK, message="Exam Name created successfully", data=ExamNameViewSerializer(instance).data)
            # If the serializer is not valid, return an error response
            return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message="Validation error", data=serializer.errors)
        except Exception as e:
            # Handle other exceptions
            return CustomResponse(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="An error occurred during the Create", data=str(e))

class ExamNameDetailsList(generics.RetrieveUpdateAPIView):
    queryset = ExamName.objects.filter(status=True)
    serializer_class = ExamNameCreateSerializer
    permission_classes = [permissions.IsAuthenticated]  # Requires a valid JWT token for access
    
    def retrieve(self, request, *args, **kwargs):
        '''Check user has permission to retrive start'''
        permission_check = check_permission(self.request.user.id, 'Exam Name', 'view')
        if not permission_check:
            return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        try:
            '''Check user has permission to retrive End'''
            instance = self.get_object()
            # Customize the response format for retrieving a single instance
            return CustomResponse(code=status.HTTP_200_OK, message="Success", data=ExamNameViewSerializer(instance).data)
        except:
            return CustomResponse(code=status.HTTP_404_NOT_FOUND, message="Not Found", data=None)

    def update(self, request, *args, **kwargs):
        '''Check user has permission to update start'''
        permission_check = check_permission(self.request.user.id, 'Exam Name', 'update')
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
                institution = institution_data if institution_data is not None else self.request.user.institution
                branch = branch_data if branch_data is not None else self.request.user.branch
                exam_name_count = ExamName.objects.filter(name=name,institution=institution,branch=branch,status=True).count()
                if (exam_name_count==0):
                    # Perform any custom update logic here if needed
                    instance = serializer.save()
                    # Customize the response format for successful update
                    return CustomResponse(code=status.HTTP_200_OK, message="Exam Name updated successfully", data=ExamNameViewSerializer(instance).data)
                return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message=f"Exam Name already exits", data=serializer.errors)
            else:
                # Handle validation errors
                return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message="Validation error", data=serializer.errors)
        except Exception as e:
            # Handle other exceptions
            return CustomResponse(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="An error occurred during the update", data=str(e))

class ExamNameDelete(generics.UpdateAPIView):
    queryset = ExamName.objects.all()
    serializer_class = ExamNameCreateSerializer
    permission_classes = [permissions.IsAuthenticated]  # Requires a valid JWT token for access
    
    def partial_update(self, request, *args, **kwargs):
        '''Check user has permission to Delete start'''
        permission_check = check_permission(self.request.user.id, 'Exam Name', 'delete')
        if not permission_check:
            return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to Delete End'''
        try:
            instance = self.get_object()
            if not instance.status:
                return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message=f"Exam Name already Deleted", data=None)
            # Update the "status" field to False
            instance.status = False
            instance.save()
            # Customize the response format for successful update
            return CustomResponse(code=status.HTTP_200_OK, message=f"Exam Name Delete successfully", data=None)
        except:
            return CustomResponse(code=status.HTTP_404_NOT_FOUND, message="Not Found", data=None)

'''
For Exam Routine
'''
class ExamRoutineList(generics.ListAPIView):
    serializer_class = ExamRoutineMstViewSerializers
    # Requires a valid JWT token for access
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = ExamRoutineMst.objects.filter(status=True).order_by('id')
        try:
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

