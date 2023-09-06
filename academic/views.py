from urllib import request
from django.shortcuts import render
from rest_framework import generics, permissions
from sms.utils import CustomResponse
from .models import *
from .serializers import *
from rest_framework import status
# from rest_framework_simplejwt.views import TokenObtainPairView
from sms.pagination import CustomPagination
from rest_framework.response import Response
from authentication.models import Authentication
# from django.contrib.auth import get_user_model

# User = get_user_model()
# Create your views here.
'''
For version
'''
class VersionList(generics.ListCreateAPIView):
    # queryset = Version.objects.filter(status=True).order_by('id')
    serializer_class = VersionSerializer
    permission_classes = [permissions.IsAuthenticated]  # Requires a valid JWT token for access
    pagination_class = CustomPagination
    
    def get_queryset(self):
        queryset = Version.objects.filter(status=True).order_by('id')
        try:
            user_id = self.request.query_params.get('user')
            users = Authentication.objects.get(id=user_id)
            if users.institution and users.branch:
                queryset = queryset.filter(institution=users.institution, branch=users.branch)
        except:
            pass
        return queryset
        
    def list(self,request,*args, **kwargs):
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
    
    def create(self, request, *args, **kwargs):
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
                return CustomResponse(code=status.HTTP_200_OK, message="Version created successfully", data=VersionSerializer(instance).data)
            # If the serializer is not valid, return an error response
            return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message="Validation error", data=serializer.errors)
        except Exception as e:
            # Handle other exceptions
            return CustomResponse(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="An error occurred during the Create", data=str(e))

class VersionDetail(generics.RetrieveUpdateAPIView):
    queryset = Version.objects.all()
    serializer_class = VersionSerializer
    permission_classes = [permissions.IsAuthenticated]  # Requires a valid JWT token for access
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        # Customize the response format for retrieving a single instance
        return CustomResponse(code=status.HTTP_200_OK, message="Success", data=VersionSerializer(instance).data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        
        try:
            if serializer.is_valid():
                # Perform any custom update logic here if needed
                instance = serializer.save()
                # Customize the response format for successful update
                return CustomResponse(code=status.HTTP_200_OK, message="Version updated successfully", data=VersionSerializer(instance).data)
            else:
                # Handle validation errors
                return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message="Validation error", data=serializer.errors)
        except Exception as e:
            # Handle other exceptions
            return CustomResponse(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="An error occurred during the update", data=str(e))
    
class VersionDelete(generics.UpdateAPIView):
    queryset = Version.objects.all()
    serializer_class = VersionSerializer
    permission_classes = [permissions.IsAuthenticated]  # Requires a valid JWT token for access
    
    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance.status:
            return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message=f"Version {instance.version} already Deleted", data=None)
        # Update the "status" field to False
        instance.status = False
        instance.save()
        # Customize the response format for successful update
        return CustomResponse(code=status.HTTP_200_OK, message=f"Version {instance.version} Delete successfully", data=None)

'''
For Session
'''
class SessionList(generics.ListCreateAPIView):
    # queryset = Version.objects.filter(status=True).order_by('id')
    serializer_class = SessionSerializer
    permission_classes = [permissions.IsAuthenticated]  # Requires a valid JWT token for access
    pagination_class = CustomPagination
    
    def get_queryset(self):
        queryset = Session.objects.filter(status=True).order_by('-id')
        try:
            institution_id = self.request.user.institution
            branch_id = self.request.user.branch
            print(branch_id)
            # users = Authentication.objects.get(id=user_id)
            if institution_id and branch_id:
                queryset = queryset.filter(institution=institution_id, branch=branch_id)
            elif branch_id:
                queryset = queryset.filter(branch=branch_id)
            elif institution_id:
                queryset = queryset.filter(institution=institution_id)
            else:
                queryset            
        except:
            pass
        return queryset
        
    def list(self,request,*args, **kwargs):
        # serializer_class = TokenObtainPairView  # Create this serializer
        if not request.user.groups.filter(name='Admin').exists():
            return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        # queryset = Session.objects.filter(status=True,institution=request.user.institution).order_by('-id')
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
                return CustomResponse(code=status.HTTP_200_OK, message="Session created successfully", data=SessionSerializer(instance).data)
            # If the serializer is not valid, return an error response
            return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message="Validation error", data=serializer.errors)
        except Exception as e:
            # Handle other exceptions
            return CustomResponse(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="An error occurred during the Create", data=str(e))

class SessionDetail(generics.RetrieveUpdateAPIView):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer
    permission_classes = [permissions.IsAuthenticated]  # Requires a valid JWT token for access
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        # Customize the response format for retrieving a single instance
        return CustomResponse(code=status.HTTP_200_OK, message="Success", data=SessionSerializer(instance).data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        
        try:
            if serializer.is_valid():
                # Perform any custom update logic here if needed
                instance = serializer.save()
                # Customize the response format for successful update
                return CustomResponse(code=status.HTTP_200_OK, message="Session updated successfully", data=SessionSerializer(instance).data)
            else:
                # Handle validation errors
                return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message="Validation error", data=serializer.errors)
        except Exception as e:
            # Handle other exceptions
            return CustomResponse(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="An error occurred during the update", data=str(e))
    
class SessionDelete(generics.UpdateAPIView):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer
    permission_classes = [permissions.IsAuthenticated]  # Requires a valid JWT token for access
    
    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance.status:
            return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message=f"Session {instance.session} already Deleted", data=None)
        # Update the "status" field to False
        instance.status = False
        instance.save()
        # Customize the response format for successful update
        return CustomResponse(code=status.HTTP_200_OK, message=f"Session {instance.session} Delete successfully", data=None)

'''
For Section
'''
class SectionList(generics.ListCreateAPIView):
    # queryset = Version.objects.filter(status=True).order_by('id')
    serializer_class = SectionSerializer
    permission_classes = [permissions.IsAuthenticated]  # Requires a valid JWT token for access
    pagination_class = CustomPagination
    
    def get_queryset(self):
        queryset = Section.objects.filter(status=True).order_by('-id')
        try:
            institution_id = self.request.user.institution
            branch_id = self.request.user.branch
            # users = Authentication.objects.get(id=user_id)
            if institution_id and branch_id:
                queryset = queryset.filter(institution=institution_id, branch=branch_id)
            elif branch_id:
                queryset = queryset.filter(branch=branch_id)
            elif institution_id:
                queryset = queryset.filter(institution=institution_id)
            else:
                queryset            
        except:
            pass
        return queryset
        
    def list(self,request,*args, **kwargs):
        # serializer_class = TokenObtainPairView  # Create this serializer
        if not request.user.groups.filter(name='Admin').exists():
            return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        # queryset = Session.objects.filter(status=True,institution=request.user.institution).order_by('-id')
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
        serializer = self.get_serializer(data=request.data)
        print(serializer)
        try:
            if serializer.is_valid():
                institution_data = serializer.validated_data.get('institution')
                branch_data = serializer.validated_data.get('branch')
                # If data is provided, use it; otherwise, use the values from the request user
                institution = institution_data if institution_data is not None else self.request.user.institution
                branch = branch_data if branch_data is not None else self.request.user.branch

                instance = serializer.save(institution=institution, branch=branch)
                # Customize the response data
                return CustomResponse(code=status.HTTP_200_OK, message="Section created successfully", data=SectionSerializer(instance).data)
            # If the serializer is not valid, return an error response
            return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message="Validation error", data=serializer.errors)
        except Exception as e:
            # Handle other exceptions
            return CustomResponse(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="An error occurred during the Create", data=str(e))

class SectionDetail(generics.RetrieveUpdateAPIView):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer
    permission_classes = [permissions.IsAuthenticated]  # Requires a valid JWT token for access
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        # Customize the response format for retrieving a single instance
        return CustomResponse(code=status.HTTP_200_OK, message="Success", data=SectionSerializer(instance).data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        
        try:
            if serializer.is_valid():
                # Perform any custom update logic here if needed
                instance = serializer.save()
                # Customize the response format for successful update
                return CustomResponse(code=status.HTTP_200_OK, message="Section updated successfully", data=SectionSerializer(instance).data)
            else:
                # Handle validation errors
                return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message="Validation error", data=serializer.errors)
        except Exception as e:
            # Handle other exceptions
            return CustomResponse(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="An error occurred during the update", data=str(e))
    
class SectionDelete(generics.UpdateAPIView):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer
    permission_classes = [permissions.IsAuthenticated]  # Requires a valid JWT token for access
    
    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance.status:
            return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message=f"Section {instance.section} already Deleted", data=None)
        # Update the "status" field to False
        instance.status = False
        instance.save()
        # Customize the response format for successful update
        return CustomResponse(code=status.HTTP_200_OK, message=f"Section {instance.section} Delete successfully", data=None)
