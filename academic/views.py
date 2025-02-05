from urllib import request
from django.shortcuts import render
from rest_framework import generics, permissions
from sms.utils import CustomResponse
from .models import *
from .serializers import *
from rest_framework import status
# from rest_framework_simplejwt.views import TokenObtainPairView
from sms.pagination import CustomPagination, CustomLimitOffsetPagination
from rest_framework.response import Response
from authentication.models import Authentication
from setup_app.models import *
from sms.permission import check_permission
from django.http import JsonResponse
from student.models import Student,StudentEnroll
# from django.contrib.auth import get_user_model

# User = get_user_model()
# Create your views here.
'''
For version
'''
class VersionViewList(generics.ListAPIView):
    # queryset = Version.objects.filter(status=True).order_by('id')
    serializer_class = VersionSerializer2
    # Requires a valid JWT token for access
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = Version.objects.filter(status=True).order_by('-id')
        try:
            institution_id = self.request.user.institution
            branch_id = self.request.user.branch
            # users = Authentication.objects.get(id=user_id)
            if institution_id and branch_id:
                queryset = queryset.filter(
                    institution=institution_id, branch=branch_id, status=True).order_by('-id')
            elif branch_id:
                queryset = queryset.filter(
                    branch=branch_id, status=True).order_by('-id')
            elif institution_id:
                queryset = queryset.filter(
                    institution=institution_id, status=True).order_by('-id')
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

class VersionList(generics.ListCreateAPIView):
    # queryset = Version.objects.filter(status=True).order_by('id')
    serializer_class = VersionSerializer
    # Requires a valid JWT token for access
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = Version.objects.filter(status=True)
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
        queryset = queryset.select_related('institution', 'branch') 
        return queryset.order_by('-id')

    def list(self, request, *args, **kwargs):
        '''Check user has permission to View start'''
        permission_check = check_permission(
            self.request.user.id, 'Version', 'view')
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
                    "count": len(queryset),
                },
            }

        return Response(response_data)

    def create(self, request, *args, **kwargs):
        '''Check user has permission to Create start'''
        permission_check = check_permission(
            self.request.user.id, 'Version', 'create')
        if not permission_check:
            return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to Create End'''

        serializer = self.get_serializer(data=request.data)
        try:
            if serializer.is_valid():
                institution_data = serializer.validated_data.get('institution')
                branch_data = serializer.validated_data.get('branch')
                version = serializer.validated_data.get('version')
                # If data is provided, use it; otherwise, use the values from the request user
                institution = institution_data if institution_data is not None else self.request.user.institution
                branch = branch_data if branch_data is not None else self.request.user.branch
                version_exists = Version.objects.filter(version=version, institution=institution, branch=branch, status=True).exists()
                if version_exists:
                    return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message=f"Version {version} already exits", data=serializer.errors)
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
    # Requires a valid JWT token for access
    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        '''Check user has permission to retrive start'''
        permission_check = check_permission(
            self.request.user.id, 'Version', 'view')
        if not permission_check:
            return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to retrive End'''

        instance = self.get_object()
        # Customize the response format for retrieving a single instance
        return CustomResponse(code=status.HTTP_200_OK, message="Success", data=VersionSerializer(instance).data)

    def update(self, request, *args, **kwargs):
        '''Check user has permission to update start'''
        permission_check = check_permission(
            self.request.user.id, 'Version', 'update')
        if not permission_check:
            return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to retrive End'''

        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)

        try:
            if serializer.is_valid():
                institution_data = serializer.validated_data.get('institution')
                branch_data = serializer.validated_data.get('branch')
                version = serializer.validated_data.get('version')
                # If data is provided, use it; otherwise, use the values from the request user
                institution = institution_data if institution_data is not None else self.request.user.institution
                branch = branch_data if branch_data is not None else self.request.user.branch
                version_count = Version.objects.filter(
                    version=version, institution=institution, branch=branch, status=True).count()
                if (version_count == 0):
                    # Perform any custom update logic here if needed
                    instance = serializer.save()
                    # Customize the response data
                    return CustomResponse(code=status.HTTP_200_OK, message="Version created successfully", data=VersionSerializer(instance).data)
                return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message=f"Version {version} already exits", data=serializer.errors)
                # Customize the response format for successful update
            else:
                # Handle validation errors
                return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message="Validation error", data=serializer.errors)
        except Exception as e:
            # Handle other exceptions
            return CustomResponse(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="An error occurred during the update", data=str(e))

class VersionDelete(generics.UpdateAPIView):
    queryset = Version.objects.all()
    serializer_class = VersionSerializer
    # Requires a valid JWT token for access
    permission_classes = [permissions.IsAuthenticated]

    def partial_update(self, request, *args, **kwargs):
        '''Check user has permission to Delete start'''
        permission_check = check_permission(
            self.request.user.id, 'Version', 'delete')
        if not permission_check:
            return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to Delete End'''

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
class SessionViewList(generics.ListAPIView):
    serializer_class = SessionSerializer2
    # Requires a valid JWT token for access
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = Session.objects.filter(status=True).order_by('-id')
        try:
            institution_id = self.request.user.institution
            branch_id = self.request.user.branch
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

class SessionList(generics.ListCreateAPIView):
    # queryset = Version.objects.filter(status=True).order_by('id')
    serializer_class = SessionSerializer
    # Requires a valid JWT token for access
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = Session.objects.filter(status=True).order_by('-id')
        try:
            institution_id = self.request.user.institution
            branch_id = self.request.user.branch
            # users = Authentication.objects.get(id=user_id)
            if institution_id and branch_id:
                queryset = queryset.filter(
                    institution=institution_id, branch=branch_id, status=True).order_by('-id')
            elif branch_id:
                queryset = queryset.filter(
                    branch=branch_id, status=True).order_by('-id')
            elif institution_id:
                queryset = queryset.filter(
                    institution=institution_id, status=True).order_by('-id')
            else:
                queryset
        except:
            pass
        return queryset

    def list(self, request, *args, **kwargs):
        '''Check user has permission to View start'''
        permission_check = check_permission(
            self.request.user.id, 'Session', 'view')
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
        permission_check = check_permission(
            self.request.user.id, 'Session', 'create')
        if not permission_check:
            return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to View end'''
        serializer = self.get_serializer(data=request.data)
        try:
            if serializer.is_valid():
                institution_data = serializer.validated_data.get('institution')
                branch_data = serializer.validated_data.get('branch')
                session = serializer.validated_data.get('session')
                # If data is provided, use it; otherwise, use the values from the request user
                institution = institution_data if institution_data is not None else self.request.user.institution
                branch = branch_data if branch_data is not None else self.request.user.branch
                session_count = Session.objects.filter(
                    session=session, institution=institution, branch=branch, status=True).count()
                if (session_count == 0):
                    instance = serializer.save(
                        institution=institution, branch=branch)
                    # Customize the response data
                    return CustomResponse(code=status.HTTP_200_OK, message="Session created successfully", data=SessionSerializer(instance).data)
                return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message=f"Session {session} already exits", data=serializer.errors)
            # If the serializer is not valid, return an error response
            return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message="Validation error", data=serializer.errors)
        except Exception as e:
            # Handle other exceptions
            return CustomResponse(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="An error occurred during the Create", data=str(e))

class SessionDetail(generics.RetrieveUpdateAPIView):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer
    # Requires a valid JWT token for access
    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        '''Check user has permission to retrive start'''
        permission_check = check_permission(
            self.request.user.id, 'Session', 'view')
        if not permission_check:
            return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to retrive End'''
        instance = self.get_object()
        # Customize the response format for retrieving a single instance
        return CustomResponse(code=status.HTTP_200_OK, message="Success", data=SessionSerializer(instance).data)

    def update(self, request, *args, **kwargs):
        '''Check user has permission to update start'''
        permission_check = check_permission(
            self.request.user.id, 'Session', 'update')
        if not permission_check:
            return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to retrive End'''
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)

        try:
            if serializer.is_valid():
                institution_data = serializer.validated_data.get('institution')
                branch_data = serializer.validated_data.get('branch')
                session = serializer.validated_data.get('session')
                institution = institution_data if institution_data is not None else self.request.user.institution
                branch = branch_data if branch_data is not None else self.request.user.branch
                session_count = Session.objects.filter(
                    session=session, institution=institution, branch=branch, status=True).count()
                if (session_count == 0):
                    # Perform any custom update logic here if needed
                    instance = serializer.save()
                    # Customize the response format for successful update
                    return CustomResponse(code=status.HTTP_200_OK, message="Session updated successfully", data=SessionSerializer(instance).data)
                return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message=f"Session {session} already exits", data=serializer.errors)
            else:
                # Handle validation errors
                return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message="Validation error", data=serializer.errors)
        except Exception as e:
            # Handle other exceptions
            return CustomResponse(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="An error occurred during the update", data=str(e))

class SessionDelete(generics.UpdateAPIView):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer
    # Requires a valid JWT token for access
    permission_classes = [permissions.IsAuthenticated]

    def partial_update(self, request, *args, **kwargs):
        '''Check user has permission to Delete start'''
        permission_check = check_permission(
            self.request.user.id, 'Session', 'delete')
        if not permission_check:
            return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to Delete End'''
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
class SectionViewList(generics.ListAPIView):
    serializer_class = SectionSerializer2
    # Requires a valid JWT token for access
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = Section.objects.filter(status=True).order_by('-id')
        try:
            institution_id = self.request.user.institution
            branch_id = self.request.user.branch
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

class SectionList(generics.ListCreateAPIView):
    # queryset = Version.objects.filter(status=True).order_by('id')
    serializer_class = SectionSerializer
    # Requires a valid JWT token for access
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = Section.objects.filter(status=True).order_by('-id')
        try:
            institution_id = self.request.user.institution
            branch_id = self.request.user.branch
            # users = Authentication.objects.get(id=user_id)
            if institution_id and branch_id:
                queryset = queryset.filter(
                    institution=institution_id, branch=branch_id, status=True).order_by('-id')
            elif branch_id:
                queryset = queryset.filter(
                    branch=branch_id, status=True).order_by('-id')
            elif institution_id:
                queryset = queryset.filter(
                    institution=institution_id, status=True).order_by('-id')
            else:
                queryset
        except:
            pass
        return queryset

    def list(self, request, *args, **kwargs):
        '''Check user has permission to View start'''
        permission_check = check_permission(
            self.request.user.id, 'Section', 'view')
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
        permission_check = check_permission(
            self.request.user.id, 'Section', 'create')
        if not permission_check:
            return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to View end'''
        serializer = self.get_serializer(data=request.data)
        try:
            if serializer.is_valid():
                institution_data = serializer.validated_data.get('institution')
                branch_data = serializer.validated_data.get('branch')
                section = serializer.validated_data.get('section')
                # If data is provided, use it; otherwise, use the values from the request user
                institution = institution_data if institution_data is not None else self.request.user.institution
                branch = branch_data if branch_data is not None else self.request.user.branch
                section_count = Section.objects.filter(
                    section=section, institution=institution, branch=branch, status=True).count()
                if (section_count == 0):
                    instance = serializer.save(
                        institution=institution, branch=branch)
                    # Customize the response data
                    return CustomResponse(code=status.HTTP_200_OK, message="Section created successfully", data=SectionSerializer(instance).data)
                return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message=f"Section {section} already exits", data=serializer.errors)
            # If the serializer is not valid, return an error response
            return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message="Validation error", data=serializer.errors)
        except Exception as e:
            # Handle other exceptions
            return CustomResponse(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="An error occurred during the Create", data=str(e))

class SectionDetail(generics.RetrieveUpdateAPIView):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer
    # Requires a valid JWT token for access
    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        '''Check user has permission to retrive start'''
        permission_check = check_permission(
            self.request.user.id, 'Section', 'view')
        if not permission_check:
            return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to retrive End'''
        instance = self.get_object()
        # Customize the response format for retrieving a single instance
        return CustomResponse(code=status.HTTP_200_OK, message="Success", data=SectionSerializer(instance).data)

    def update(self, request, *args, **kwargs):
        '''Check user has permission to update start'''
        permission_check = check_permission(
            self.request.user.id, 'Section', 'update')
        if not permission_check:
            return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to retrive End'''
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)

        try:
            if serializer.is_valid():
                institution_data = serializer.validated_data.get('institution')
                branch_data = serializer.validated_data.get('branch')
                section = serializer.validated_data.get('section')
                institution = institution_data if institution_data is not None else self.request.user.institution
                branch = branch_data if branch_data is not None else self.request.user.branch
                section_count = Section.objects.filter(
                    section=section, institution=institution, branch=branch, status=True).count()
                if (section_count == 0):
                    # Perform any custom update logic here if needed
                    instance = serializer.save()
                    # Customize the response format for successful update
                    return CustomResponse(code=status.HTTP_200_OK, message="Section updated successfully", data=SectionSerializer(instance).data)
                return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message=f"Section {section} already exits", data=serializer.errors)
            else:
                # Handle validation errors
                return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message="Validation error", data=serializer.errors)
        except Exception as e:
            # Handle other exceptions
            return CustomResponse(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="An error occurred during the update", data=str(e))

class SectionDelete(generics.UpdateAPIView):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer
    # Requires a valid JWT token for access
    permission_classes = [permissions.IsAuthenticated]

    def partial_update(self, request, *args, **kwargs):
        '''Check user has permission to Delete start'''
        permission_check = check_permission(
            self.request.user.id, 'Section', 'delete')
        if not permission_check:
            return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to Delete End'''
        instance = self.get_object()
        if not instance.status:
            return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message=f"Section {instance.section} already Deleted", data=None)
        # Update the "status" field to False
        instance.status = False
        instance.save()
        # Customize the response format for successful update
        return CustomResponse(code=status.HTTP_200_OK, message=f"Section {instance.section} Delete successfully", data=None)

'''
For Subject
'''
class SubjectViewList(generics.ListAPIView):
    serializer_class = SubjectListViewSerializer
    # Requires a valid JWT token for access
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = Subject.objects.filter(status=True).order_by('id')
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

class SubjectList(generics.ListCreateAPIView):
    # queryset = Version.objects.filter(status=True).order_by('id')
    serializer_class = SubjectSerializer
    # Requires a valid JWT token for access
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = Subject.objects.filter(status=True).order_by('-id')
        try:
            institution_id = self.request.user.institution
            branch_id = self.request.user.branch
            # users = Authentication.objects.get(id=user_id)
            if institution_id and branch_id:
                queryset = queryset.filter(
                    institution=institution_id, branch=branch_id, status=True).order_by('-id')
            elif branch_id:
                queryset = queryset.filter(
                    branch=branch_id, status=True).order_by('-id')
            elif institution_id:
                queryset = queryset.filter(
                    institution=institution_id, status=True).order_by('-id')
            else:
                queryset
        except:
            pass
        return queryset

    def list(self, request, *args, **kwargs):
        '''Check user has permission to View start'''
        permission_check = check_permission(
            self.request.user.id, 'Subject', 'view')
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
        permission_check = check_permission(
            self.request.user.id, 'Subject', 'create')
        if not permission_check:
            return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to View end'''
        serializer_class = SubjectSerializer3
        serializer = serializer_class(data=request.data)
        try:
            if serializer.is_valid():
                institution_data = serializer.validated_data.get('institution')
                branch_data = serializer.validated_data.get('branch')
                code = serializer.validated_data.get('code')
                type = serializer.validated_data.get('type')
                name = serializer.validated_data.get('name')
                # If data is provided, use it; otherwise, use the values from the request user
                institution = institution_data if institution_data is not None else self.request.user.institution
                branch = branch_data if branch_data is not None else self.request.user.branch
                subject_count = Subject.objects.filter(
                    code=code, type=type, name=name, institution=institution, branch=branch, status=True).count()
                if (subject_count == 0):
                    instance = serializer.save(
                        institution=institution, branch=branch)
                    # Customize the response data
                    return CustomResponse(code=status.HTTP_200_OK, message="Subject created successfully", data=SubjectSerializer(instance).data)
                return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message=f"Subject {name} {type} already exits", data=serializer.errors)
            # If the serializer is not valid, return an error response
            return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message="Validation error", data=serializer.errors)
        except Exception as e:
            # Handle other exceptions
            return CustomResponse(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="An error occurred during the Create", data=str(e))

class SubjectDetail(generics.RetrieveUpdateAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    # Requires a valid JWT token for access
    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        '''Check user has permission to View start'''
        permission_check = check_permission(
            self.request.user.id, 'Subject', 'view')
        if not permission_check:
            return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to View end'''
        instance = self.get_object()
        # Customize the response format for retrieving a single instance
        return CustomResponse(code=status.HTTP_200_OK, message="Success", data=SubjectSerializer(instance).data)

    def update(self, request, *args, **kwargs):
        '''Check user has permission to View start'''
        permission_check = check_permission(
            self.request.user.id, 'Subject', 'update')
        if not permission_check:
            return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to View end'''
        partial = kwargs.pop('partial', False)
        serializer_class = SubjectSerializer3
        instance = self.get_object()
        serializer = serializer_class(
            instance, data=request.data, partial=partial)

        try:
            if serializer.is_valid():
                institution_data = serializer.validated_data.get('institution')
                branch_data = serializer.validated_data.get('branch')
                code = serializer.validated_data.get('code')
                type = serializer.validated_data.get('type')
                name = serializer.validated_data.get('name')
                # If data is provided, use it; otherwise, use the values from the request user
                institution = institution_data if institution_data is not None else self.request.user.institution
                branch = branch_data if branch_data is not None else self.request.user.branch
                subject_count = Subject.objects.filter(
                    code=code, type=type, name=name, institution=institution, branch=branch, status=True).count()
                if (subject_count == 0):
                    # Perform any custom update logic here if needed
                    instance = serializer.save()
                    # Customize the response format for successful update
                    return CustomResponse(code=status.HTTP_200_OK, message="Subject updated successfully", data=SubjectSerializer(instance).data)
                return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message=f"Subject {name} {type} already exits", data=serializer.errors)
            else:
                # Handle validation errors
                return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message="Validation error", data=serializer.errors)
        except Exception as e:
            # Handle other exceptions
            return CustomResponse(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="An error occurred during the update", data=str(e))

class SubjectDelete(generics.UpdateAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    # Requires a valid JWT token for access
    permission_classes = [permissions.IsAuthenticated]

    def partial_update(self, request, *args, **kwargs):
        '''Check user has permission to View start'''
        permission_check = check_permission(
            self.request.user.id, 'Subject', 'delete')
        if not permission_check:
            return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to View end'''
        instance = self.get_object()
        if not instance.status:
            return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message=f"Subject {instance.name} already Deleted", data=None)
        # Update the "status" field to False
        instance.status = False
        instance.save()
        # Customize the response format for successful update
        return CustomResponse(code=status.HTTP_200_OK, message=f"Subject {instance.name} Delete successfully", data=None)

'''
For Class
'''
class ClassViewList(generics.ListAPIView):
    serializer_class = ClassSerializer2
    # Requires a valid JWT token for access
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = ClassName.objects.filter(status=True).order_by('id')
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

class ClassList(generics.ListCreateAPIView):
    # queryset = Version.objects.filter(status=True).order_by('id')
    serializer_class = ClassSerializer
    # Requires a valid JWT token for access
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = ClassName.objects.filter(status=True).order_by('-id')
        try:
            institution_id = self.request.user.institution
            branch_id = self.request.user.branch
            # users = Authentication.objects.get(id=user_id)
            if institution_id and branch_id:
                queryset = queryset.filter(
                    institution=institution_id, branch=branch_id, status=True).order_by('-id')
            elif branch_id:
                queryset = queryset.filter(
                    branch=branch_id, status=True).order_by('-id')
            elif institution_id:
                queryset = queryset.filter(
                    institution=institution_id, status=True).order_by('-id')
            else:
                queryset
        except:
            pass
        return queryset

    def list(self, request, *args, **kwargs):
        '''Check user has permission to View start'''
        permission_check = check_permission(
            self.request.user.id, 'Class', 'view')
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
        permission_check = check_permission(
            self.request.user.id, 'Class', 'create')
        if not permission_check:
            return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to View end'''
        serializer = self.get_serializer(data=request.data)
        try:
            if serializer.is_valid():
                institution_data = serializer.validated_data.get('institution')
                branch_data = serializer.validated_data.get('branch')
                name = serializer.validated_data.get('name')
                # If data is provided, use it; otherwise, use the values from the request user
                institution = institution_data if institution_data is not None else self.request.user.institution
                branch = branch_data if branch_data is not None else self.request.user.branch
                class_count = ClassName.objects.filter(
                    name=name, institution=institution, branch=branch, status=True).count()
                if (class_count == 0):
                    instance = serializer.save(
                        institution=institution, branch=branch)
                    # Customize the response data
                    return CustomResponse(code=status.HTTP_200_OK, message="Class created successfully", data=ClassSerializer(instance).data)
                return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message=f"Class {name} already exits", data=serializer.errors)
            # If the serializer is not valid, return an error response
            return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message="Validation error", data=serializer.errors)
        except Exception as e:
            # Handle other exceptions
            return CustomResponse(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="An error occurred during the Create", data=str(e))

class ClassDetail(generics.RetrieveUpdateAPIView):
    queryset = ClassName.objects.all()
    serializer_class = ClassSerializer
    # Requires a valid JWT token for access
    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        '''Check user has permission to View start'''
        permission_check = check_permission(
            self.request.user.id, 'Class', 'view')
        if not permission_check:
            return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to View end'''
        instance = self.get_object()
        # Customize the response format for retrieving a single instance
        return CustomResponse(code=status.HTTP_200_OK, message="Success", data=ClassSerializer(instance).data)

    def update(self, request, *args, **kwargs):
        '''Check user has permission to View start'''
        permission_check = check_permission(
            self.request.user.id, 'Class', 'update')
        if not permission_check:
            return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to View end'''
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)

        try:
            if serializer.is_valid():
                institution_data = serializer.validated_data.get('institution')
                branch_data = serializer.validated_data.get('branch')
                name = serializer.validated_data.get('name')
                # If data is provided, use it; otherwise, use the values from the request user
                institution = institution_data if institution_data is not None else self.request.user.institution
                branch = branch_data if branch_data is not None else self.request.user.branch
                class_count = ClassName.objects.filter(
                    name=name, institution=institution, branch=branch, status=True).count()
                if (class_count == 0):
                    # Perform any custom update logic here if needed
                    instance = serializer.save()
                    # Customize the response format for successful update
                    return CustomResponse(code=status.HTTP_200_OK, message="Class {name} updated successfully", data=ClassSerializer(instance).data)
                return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message=f"Class {name} already exits", data=serializer.errors)
            else:
                # Handle validation errors
                return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message="Validation error", data=serializer.errors)
        except Exception as e:
            # Handle other exceptions
            return CustomResponse(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="An error occurred during the update", data=str(e))

class ClassDelete(generics.UpdateAPIView):
    queryset = ClassName.objects.all()
    serializer_class = ClassSerializer
    # Requires a valid JWT token for access
    permission_classes = [permissions.IsAuthenticated]

    def partial_update(self, request, *args, **kwargs):
        '''Check user has permission to View start'''
        permission_check = check_permission(
            self.request.user.id, 'Class', 'delete')
        if not permission_check:
            return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to View end'''
        instance = self.get_object()
        if not instance.status:
            return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message=f"Class {instance.name} already Deleted", data=None)
        # Update the "status" field to False
        instance.status = False
        instance.save()
        # Customize the response format for successful update
        return CustomResponse(code=status.HTTP_200_OK, message=f"Class {instance.name} Delete successfully", data=None)

'''
For Class Room
'''
class ClassRoomViewList(generics.ListAPIView):
    serializer_class = ClassRoomViewSerializer
    # Requires a valid JWT token for access
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = ClassRoom.objects.filter(status=True).order_by('id')
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

class ClassRoomList(generics.ListCreateAPIView):
    # queryset = Version.objects.filter(status=True).order_by('id')
    serializer_class = ClassRoomSerializer
    # Requires a valid JWT token for access
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = ClassRoom.objects.filter(status=True).order_by('-id')
        try:
            institution_id = self.request.user.institution
            branch_id = self.request.user.branch
            # users = Authentication.objects.get(id=user_id)
            if institution_id and branch_id:
                queryset = queryset.filter(
                    institution=institution_id, branch=branch_id, status=True).order_by('-id')
            elif branch_id:
                queryset = queryset.filter(
                    branch=branch_id, status=True).order_by('-id')
            elif institution_id:
                queryset = queryset.filter(
                    institution=institution_id, status=True).order_by('-id')
            else:
                queryset
        except:
            pass
        return queryset

    def list(self, request, *args, **kwargs):
        '''Check user has permission to View start'''
        permission_check = check_permission(
            self.request.user.id, 'Class Room', 'view')
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
        permission_check = check_permission(
            self.request.user.id, 'Class Room', 'create')
        if not permission_check:
            return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to View end'''
        serializer_class = ClassRoomSerializer3
        serializer = serializer_class(data=request.data)
        try:
            if serializer.is_valid():
                institution_data = serializer.validated_data.get('institution')
                branch_data = serializer.validated_data.get('branch')
                floor_type = serializer.validated_data.get('floor_type')
                building = serializer.validated_data.get('building')
                room_no = serializer.validated_data.get('room_no')
                # If data is provided, use it; otherwise, use the values from the request user
                institution = institution_data if institution_data is not None else self.request.user.institution
                branch = branch_data if branch_data is not None else self.request.user.branch
                class_room_count = ClassRoom.objects.filter(
                    floor_type=floor_type, building=building, room_no=room_no, institution=institution, branch=branch, status=True).count()
                if (class_room_count == 0):
                    instance = serializer.save(
                        institution=institution, branch=branch)
                    # Customize the response data
                    return CustomResponse(code=status.HTTP_200_OK, message="Class Room created successfully", data=ClassRoomSerializer(instance).data)
                return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message=f"Class Room already exits", data=serializer.errors)
            # If the serializer is not valid, return an error response
            return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message="Validation error", data=serializer.errors)
        except Exception as e:
            # Handle other exceptions
            return CustomResponse(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="An error occurred during the Create", data=str(e))

class ClassRoomDetail(generics.RetrieveUpdateAPIView):
    queryset = ClassRoom.objects.all()
    serializer_class = ClassRoomSerializer
    # Requires a valid JWT token for access
    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        '''Check user has permission to View start'''
        permission_check = check_permission(
            self.request.user.id, 'Class Room', 'view')
        if not permission_check:
            return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to View end'''
        instance = self.get_object()
        # Customize the response format for retrieving a single instance
        return CustomResponse(code=status.HTTP_200_OK, message="Success", data=ClassRoomSerializer(instance).data)

    def update(self, request, *args, **kwargs):
        '''Check user has permission to View start'''
        permission_check = check_permission(
            self.request.user.id, 'Class Room', 'delete')
        if not permission_check:
            return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to View end'''
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer_class = ClassRoomSerializer3
        serializer = serializer_class(
            instance, data=request.data, partial=partial)

        try:
            if serializer.is_valid():
                institution_data = serializer.validated_data.get('institution')
                branch_data = serializer.validated_data.get('branch')
                floor_type = serializer.validated_data.get('floor_type')
                building = serializer.validated_data.get('building')
                room_no = serializer.validated_data.get('room_no')
                # If data is provided, use it; otherwise, use the values from the request user
                institution = institution_data if institution_data is not None else self.request.user.institution
                branch = branch_data if branch_data is not None else self.request.user.branch
                class_room_count = ClassRoom.objects.filter(
                    floor_type=floor_type, building=building, room_no=room_no, institution=institution, branch=branch, status=True).count()
                if (class_room_count == 0):
                    # Perform any custom update logic here if needed
                    instance = serializer.save()
                    # Customize the response format for successful update
                    return CustomResponse(code=status.HTTP_200_OK, message="Class Room updated successfully", data=ClassRoomSerializer(instance).data)
                return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message=f"Class Room already exits", data=serializer.errors)
            else:
                # Handle validation errors
                return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message="Validation error", data=serializer.errors)
        except Exception as e:
            # Handle other exceptions
            return CustomResponse(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="An error occurred during the update", data=str(e))

class ClassRoomDelete(generics.UpdateAPIView):
    queryset = ClassRoom.objects.all()
    serializer_class = ClassRoomSerializer3
    # Requires a valid JWT token for access
    permission_classes = [permissions.IsAuthenticated]

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance.status:
            return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message=f"Class Room {instance.room_no} already Deleted", data=None)
        # Update the "status" field to False
        instance.status = False
        instance.save()
        # Customize the response format for successful update
        return CustomResponse(code=status.HTTP_200_OK, message=f"Class Room {instance.room_no} Delete successfully", data=None)

'''
For Class Period
'''
class ClassPeriodViewList(generics.ListAPIView):
    serializer_class = ClassPeriodSerializer2
    # Requires a valid JWT token for access
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = ClassPeriod.objects.filter(status=True).order_by('id')
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

class ClassPeriodList(generics.ListCreateAPIView):
    # queryset = Version.objects.filter(status=True).order_by('id')
    serializer_class = ClassPeriodSerializer
    # Requires a valid JWT token for access
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = ClassPeriod.objects.filter(status=True).order_by('-id')
        try:
            institution_id = self.request.user.institution
            branch_id = self.request.user.branch
            # users = Authentication.objects.get(id=user_id)
            if institution_id and branch_id:
                queryset = queryset.filter(
                    institution=institution_id, branch=branch_id, status=True).order_by('-id')
            elif branch_id:
                queryset = queryset.filter(
                    branch=branch_id, status=True).order_by('-id')
            elif institution_id:
                queryset = queryset.filter(
                    institution=institution_id, status=True).order_by('-id')
            else:
                queryset
        except:
            pass
        return queryset

    def list(self, request, *args, **kwargs):
        '''Check user has permission to View start'''
        permission_check = check_permission(
            self.request.user.id, 'Class Period', 'view')
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
        permission_check = check_permission(
            self.request.user.id, 'Class Period', 'create')
        if not permission_check:
            return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to View end'''
        serializer = self.get_serializer(data=request.data)
        try:
            if serializer.is_valid():
                institution_data = serializer.validated_data.get('institution')
                branch_data = serializer.validated_data.get('branch')
                start_time = serializer.validated_data.get('start_time')
                end_time = serializer.validated_data.get('end_time')
                # If data is provided, use it; otherwise, use the values from the request user
                institution = institution_data if institution_data is not None else self.request.user.institution
                branch = branch_data if branch_data is not None else self.request.user.branch
                class_period_count = ClassPeriod.objects.filter(
                    start_time=start_time, end_time=end_time, institution=institution, branch=branch, status=True).count()
                if (class_period_count == 0):
                    instance = serializer.save(
                        institution=institution, branch=branch)
                    # Customize the response data
                    return CustomResponse(code=status.HTTP_200_OK, message="Class Period created successfully", data=ClassPeriodSerializer(instance).data)
                return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message=f"Class Period already exits", data=serializer.errors)
            # If the serializer is not valid, return an error response
            return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message="Validation error", data=serializer.errors)
        except Exception as e:
            # Handle other exceptions
            return CustomResponse(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="An error occurred during the Create", data=str(e))

class ClassPeriodDetail(generics.RetrieveUpdateAPIView):
    queryset = ClassPeriod.objects.all()
    serializer_class = ClassPeriodSerializer
    # Requires a valid JWT token for access
    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        '''Check user has permission to View start'''
        permission_check = check_permission(
            self.request.user.id, 'Class Period', 'view')
        if not permission_check:
            return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to View end'''
        instance = self.get_object()
        # Customize the response format for retrieving a single instance
        return CustomResponse(code=status.HTTP_200_OK, message="Success", data=ClassPeriodSerializer(instance).data)

    def update(self, request, *args, **kwargs):
        '''Check user has permission to View start'''
        permission_check = check_permission(
            self.request.user.id, 'Class Period', 'update')
        if not permission_check:
            return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to View end'''
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)

        try:
            if serializer.is_valid():
                institution_data = serializer.validated_data.get('institution')
                branch_data = serializer.validated_data.get('branch')
                start_time = serializer.validated_data.get('start_time')
                end_time = serializer.validated_data.get('end_time')
                # If data is provided, use it; otherwise, use the values from the request user
                institution = institution_data if institution_data is not None else self.request.user.institution
                branch = branch_data if branch_data is not None else self.request.user.branch
                class_period_count = ClassPeriod.objects.filter(
                    start_time=start_time, end_time=end_time, institution=institution, branch=branch, status=True).count()
                if (class_period_count == 0):
                    # Perform any custom update logic here if needed
                    instance = serializer.save()
                    # Customize the response format for successful update
                    return CustomResponse(code=status.HTTP_200_OK, message="Class Period updated successfully", data=ClassPeriodSerializer(instance).data)
                return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message=f"Class Period already exits", data=serializer.errors)
            else:
                # Handle validation errors
                return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message="Validation error", data=serializer.errors)
        except Exception as e:
            # Handle other exceptions
            return CustomResponse(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="An error occurred during the update", data=str(e))

class ClassPeriodDelete(generics.UpdateAPIView):
    queryset = ClassPeriod.objects.all()
    serializer_class = ClassPeriodSerializer
    # Requires a valid JWT token for access
    permission_classes = [permissions.IsAuthenticated]

    def partial_update(self, request, *args, **kwargs):
        '''Check user has permission to View start'''
        permission_check = check_permission(
            self.request.user.id, 'Class Period', 'delete')
        if not permission_check:
            return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to View end'''
        instance = self.get_object()
        if not instance.status:
            return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message=f"Class Period {instance.name} already Deleted", data=None)
        # Update the "status" field to False
        instance.status = False
        instance.save()
        # Customize the response format for successful update
        return CustomResponse(code=status.HTTP_200_OK, message=f"Class Period {instance.name} Delete successfully", data=None)

'''
For Class Section
'''
class ClassSectionViewList(generics.ListAPIView):
    serializer_class = ClassSectionViewSerializer
    # Requires a valid JWT token for access
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = ClassSection.objects.filter(status=True).order_by('id')
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

class ClassSectionList(generics.ListCreateAPIView):
    # queryset = Version.objects.filter(status=True).order_by('id')
    serializer_class = ClassSectionSerializer
    # Requires a valid JWT token for access
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = ClassSection.objects.filter(status=True).order_by('-id')
        try:
            institution_id = self.request.user.institution
            branch_id = self.request.user.branch
            # users = Authentication.objects.get(id=user_id)
            if institution_id and branch_id:
                queryset = queryset.filter(
                    institution=institution_id, branch=branch_id, status=True).order_by('-id')
            elif branch_id:
                queryset = queryset.filter(
                    branch=branch_id, status=True).order_by('-id')
            elif institution_id:
                queryset = queryset.filter(
                    institution=institution_id, status=True).order_by('-id')
            else:
                queryset
        except:
            pass
        return queryset

    def list(self, request, *args, **kwargs):
        '''Check user has permission to View start'''
        permission_check = check_permission(
            self.request.user.id, 'Class Section', 'view')
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
        permission_check = check_permission(
            self.request.user.id, 'Class Section', 'create')
        if not permission_check:
            return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to View end'''
        serializer_class = ClassSectionSerializer3
        serializer = serializer_class(data=request.data)
        try:
            if serializer.is_valid():
                institution_data = serializer.validated_data.get('institution')
                branch_data = serializer.validated_data.get('branch')
                class_name = serializer.validated_data.get('class_name')
                section = serializer.validated_data.get('section')
                session = serializer.validated_data.get('session')
                version = serializer.validated_data.get('version')
                # If data is provided, use it; otherwise, use the values from the request user
                institution = institution_data if institution_data is not None else self.request.user.institution
                branch = branch_data if branch_data is not None else self.request.user.branch
                class_section_count = ClassSection.objects.filter(
                    class_name=class_name, section=section, session=session, version=version, institution=institution, branch=branch, status=True).count()
                if (class_section_count == 0):
                    instance = serializer.save(
                        institution=institution, branch=branch)
                    # Customize the response data
                    return CustomResponse(code=status.HTTP_200_OK, message="Class Section created successfully", data=ClassSectionSerializer(instance).data)
                return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message=f"Class Section already exits", data=serializer.errors)
            # If the serializer is not valid, return an error response
            return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message="Validation error", data=serializer.errors)
        except Exception as e:
            # Handle other exceptions
            return CustomResponse(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="An error occurred during the Create", data=str(e))

class ClassSectionDetail(generics.RetrieveUpdateAPIView):
    queryset = ClassSection.objects.all()
    serializer_class = ClassSectionSerializer
    # Requires a valid JWT token for access
    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        '''Check user has permission to View start'''
        permission_check = check_permission(
            self.request.user.id, 'Class Section', 'view')
        if not permission_check:
            return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to View end'''
        instance = self.get_object()
        # Customize the response format for retrieving a single instance
        return CustomResponse(code=status.HTTP_200_OK, message="Success", data=ClassSectionSerializer(instance).data)

    def update(self, request, *args, **kwargs):
        '''Check user has permission to View start'''
        permission_check = check_permission(
            self.request.user.id, 'Class Section', 'update')
        if not permission_check:
            return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to View end'''
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer_class = ClassSectionSerializer3
        serializer = serializer_class(
            instance, data=request.data, partial=partial)

        try:
            if serializer.is_valid():
                institution_data = serializer.validated_data.get('institution')
                branch_data = serializer.validated_data.get('branch')
                class_name = serializer.validated_data.get('class_name')
                section = serializer.validated_data.get('section')
                session = serializer.validated_data.get('session')
                version = serializer.validated_data.get('version')
                # If data is provided, use it; otherwise, use the values from the request user
                institution = institution_data if institution_data is not None else self.request.user.institution
                branch = branch_data if branch_data is not None else self.request.user.branch
                class_section_count = ClassSection.objects.filter(class_name=class_name, section=section, session=session, version=version, institution=institution, branch=branch, status=True).count()
                if (class_section_count == 0):
                    # Perform any custom update logic here if needed
                    instance = serializer.save()
                    # Customize the response format for successful update
                    return CustomResponse(code=status.HTTP_200_OK, message="Class Section updated successfully", data=ClassSectionSerializer(instance).data)
                return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message=f"Class Section already exits", data=serializer.errors)
            else:
                # Handle validation errors
                return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message="Validation error", data=serializer.errors)
        except Exception as e:
            # Handle other exceptions
            return CustomResponse(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="An error occurred during the update", data=str(e))

class ClassSectionDelete(generics.UpdateAPIView):
    queryset = ClassSection.objects.all()
    serializer_class = ClassSectionSerializer
    # Requires a valid JWT token for access
    permission_classes = [permissions.IsAuthenticated]

    def partial_update(self, request, *args, **kwargs):
        '''Check user has permission to View start'''
        permission_check = check_permission(
            self.request.user.id, 'Class Section', 'delete')
        if not permission_check:
            return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to View end'''
        instance = self.get_object()
        if not instance.status:
            return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message=f"Class Section {instance.class_name} {instance.section} already Deleted", data=None)
        # Update the "status" field to False
        instance.status = False
        instance.save()
        # Customize the response format for successful update
        return CustomResponse(code=status.HTTP_200_OK, message=f"Class Section {instance.class_name} {instance.section} Delete successfully", data=None)

'''
For Class Subject
'''
class ClassSubjectViewList(generics.ListAPIView):
    serializer_class = ClassSubjectViewSerializer
    # Requires a valid JWT token for access
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        session = self.request.query_params.get('session')
        version = self.request.query_params.get('version')
        class_name = self.request.query_params.get('class_name')
        section = self.request.query_params.get('section')
        if class_name and section and version and session:
            queryset = ClassSubject.objects.filter(status=True,session=session,version=version,class_name=class_name,section=section).order_by('id')
        else:
            queryset = ClassSubject.objects.filter(status=True).order_by('id')
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

class ClassSubjectList(generics.ListCreateAPIView):
    # queryset = Version.objects.filter(status=True).order_by('id')
    serializer_class = ClassSubjectSerializer
    # Requires a valid JWT token for access
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = ClassSubject.objects.filter(status=True).order_by('-id')
        try:
            institution_id = self.request.user.institution
            branch_id = self.request.user.branch
            # users = Authentication.objects.get(id=user_id)
            if institution_id and branch_id:
                queryset = queryset.filter(
                    institution=institution_id, branch=branch_id, status=True).order_by('-id')
            elif branch_id:
                queryset = queryset.filter(
                    branch=branch_id, status=True).order_by('-id')
            elif institution_id:
                queryset = queryset.filter(
                    institution=institution_id, status=True).order_by('-id')
            else:
                queryset
        except:
            pass
        return queryset

    def list(self, request, *args, **kwargs):
        '''Check user has permission to View start'''
        permission_check = check_permission(
            self.request.user.id, 'Class Subject', 'view')
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
        permission_check = check_permission(
            self.request.user.id, 'Class Subject', 'create')
        if not permission_check:
            return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to View end'''
        serializer_class = ClassSubjectSerializer2
        serializer = serializer_class(data=request.data)
        try:
            if serializer.is_valid():
                institution_data = serializer.validated_data.get('institution')
                branch_data = serializer.validated_data.get('branch')
                class_name = serializer.validated_data.get('class_name')
                section = serializer.validated_data.get('section')
                session = serializer.validated_data.get('session')
                version = serializer.validated_data.get('version')
                code = serializer.validated_data.get('code')
                subject = serializer.validated_data.get('subject')
                # If data is provided, use it; otherwise, use the values from the request user
                institution = institution_data if institution_data is not None else self.request.user.institution
                branch = branch_data if branch_data is not None else self.request.user.branch
                class_sub_count = ClassSubject.objects.filter(class_name=class_name, section=section, session=session,
                                                              version=version, code=code, subject=subject, institution=institution, branch=branch, status=True).count()
                if (class_sub_count == 0):
                    instance = serializer.save(
                        institution=institution, branch=branch)
                    # Customize the response data
                    return CustomResponse(code=status.HTTP_200_OK, message="Class Subject created successfully", data=ClassSubjectSerializer(instance).data)
                return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message=f"Class Subject already exits", data=serializer.errors)
            # If the serializer is not valid, return an error response
            return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message="Validation error", data=serializer.errors)
        except Exception as e:
            # Handle other exceptions
            return CustomResponse(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="An error occurred during the Create", data=str(e))

class ClassSubjectDetail(generics.RetrieveUpdateAPIView):
    queryset = ClassSubject.objects.all()
    serializer_class = ClassSubjectSerializer
    # Requires a valid JWT token for access
    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        '''Check user has permission to View start'''
        permission_check = check_permission(
            self.request.user.id, 'Class Subject', 'view')
        if not permission_check:
            return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to View end'''
        instance = self.get_object()
        # Customize the response format for retrieving a single instance
        return CustomResponse(code=status.HTTP_200_OK, message="Success", data=ClassSubjectSerializer(instance).data)

    def update(self, request, *args, **kwargs):
        '''Check user has permission to View start'''
        permission_check = check_permission(
            self.request.user.id, 'Class Subject', 'update')
        if not permission_check:
            return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to View end'''
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer_class = ClassSubjectSerializer2
        serializer = serializer_class(
            instance, data=request.data, partial=partial)

        try:
            if serializer.is_valid():
                institution_data = serializer.validated_data.get('institution')
                branch_data = serializer.validated_data.get('branch')
                class_name = serializer.validated_data.get('class_name')
                section = serializer.validated_data.get('section')
                session = serializer.validated_data.get('session')
                version = serializer.validated_data.get('version')
                code = serializer.validated_data.get('code')
                subject = serializer.validated_data.get('subject')
                # If data is provided, use it; otherwise, use the values from the request user
                institution = institution_data if institution_data is not None else self.request.user.institution
                branch = branch_data if branch_data is not None else self.request.user.branch
                class_sub_count = ClassSubject.objects.filter(class_name=class_name, section=section, session=session,
                                                              version=version, code=code, subject=subject, institution=institution, branch=branch, status=True).count()
                if (class_sub_count == 0):
                    # Perform any custom update logic here if needed
                    instance = serializer.save()
                    # Customize the response format for successful update
                    return CustomResponse(code=status.HTTP_200_OK, message="Class Subject updated successfully", data=ClassSubjectSerializer(instance).data)
                return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message=f"Class Subject already exits", data=serializer.errors)
            else:
                # Handle validation errors
                return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message="Validation error", data=serializer.errors)
        except Exception as e:
            # Handle other exceptions
            return CustomResponse(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="An error occurred during the update", data=str(e))

class ClassSubjectDelete(generics.UpdateAPIView):
    queryset = ClassSubject.objects.all()
    serializer_class = ClassSubjectSerializer
    # Requires a valid JWT token for access
    permission_classes = [permissions.IsAuthenticated]

    def partial_update(self, request, *args, **kwargs):
        '''Check user has permission to View start'''
        permission_check = check_permission(
            self.request.user.id, 'Class Subject', 'delete')
        if not permission_check:
            return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to View end'''
        instance = self.get_object()
        if not instance.status:
            return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message=f"Class Subject {instance.subject} already Deleted", data=None)
        # Update the "status" field to False
        instance.status = False
        instance.save()
        # Customize the response format for successful update
        return CustomResponse(code=status.HTTP_200_OK, message=f"Class Section {instance.subject} Delete successfully", data=None)

'''
For Class Routine
'''

class ClassRoutineCreateList(generics.ListCreateAPIView):
    serializer_class = ClassRoutineSerializer
    # Requires a valid JWT token for access
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = ClassRoutine.objects.filter(status=True).order_by('-id')
        try:
            institution_id = self.request.user.institution
            branch_id = self.request.user.branch
            # users = Authentication.objects.get(id=user_id)
            if institution_id and branch_id:
                queryset = queryset.filter(
                    institution=institution_id, branch=branch_id, status=True).order_by('-id')
            elif branch_id:
                queryset = queryset.filter(
                    branch=branch_id, status=True).order_by('-id')
            elif institution_id:
                queryset = queryset.filter(
                    institution=institution_id, status=True).order_by('-id')
            else:
                queryset
        except:
            pass
        return queryset

    def list(self, request, *args, **kwargs):
        '''Check user has permission to View start'''
        permission_check = check_permission(
            self.request.user.id, 'Class Routine', 'view')
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
        permission_check = check_permission(
            self.request.user.id, 'Class Routine', 'create')
        if not permission_check:
            return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to View end'''
        serializer_class = ClassRoutineSerializer2
        serializer = serializer_class(data=request.data)
        try:
            if serializer.is_valid():
                institution_data = serializer.validated_data.get('institution')
                branch_data = serializer.validated_data.get('branch')
                teacher = serializer.validated_data.get('teacher')
                class_name = serializer.validated_data.get('class_name')
                section = serializer.validated_data.get('section')
                session = serializer.validated_data.get('session')
                version = serializer.validated_data.get('version')
                subject = serializer.validated_data.get('subject')
                class_period = serializer.validated_data.get('class_period')
                day = serializer.validated_data.get('day')
                class_room = serializer.validated_data.get('class_room')
                # If data is provided, use it; otherwise, use the values from the request user
                institution = institution_data if institution_data is not None else self.request.user.institution
                branch = branch_data if branch_data is not None else self.request.user.branch
                routine_count = ClassRoutine.objects.filter(class_room=class_room, day=day, class_period=class_period, teacher=teacher, class_name=class_name,
                                                            section=section, session=session, version=version, subject=subject, institution=institution, branch=branch, status=True)
                if (routine_count == 0):
                    instance = serializer.save(
                        institution=institution, branch=branch)
                    # Customize the response data
                    return CustomResponse(code=status.HTTP_200_OK, message="Class Routine created successfully", data=ClassRoutineSerializer(instance).data)
                return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message="Class Routine already exists", data=serializer.errors)
            # If the serializer is not valid, return an error response
            return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message="Validation error", data=serializer.errors)
        except Exception as e:
            # Handle other exceptions
            return CustomResponse(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="An error occurred during the Create", data=str(e))

class ClassRoutineDetail(generics.RetrieveUpdateAPIView):
    queryset = ClassRoutine.objects.filter(status=True)
    serializer_class = ClassRoutineSerializer
    # Requires a valid JWT token for access
    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        '''Check user has permission to retrive start'''
        permission_check = check_permission(
            self.request.user.id, 'Class Routine', 'view')
        if not permission_check:
            return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        try:
            '''Check user has permission to retrive End'''
            instance = self.get_object()
            # Customize the response format for retrieving a single instance
            return CustomResponse(code=status.HTTP_200_OK, message="Success", data=ClassRoutineSerializer(instance).data)
        except:
            return CustomResponse(code=status.HTTP_404_NOT_FOUND, message="Not Found", data=None)

    def update(self, request, *args, **kwargs):
        '''Check user has permission to update start'''
        permission_check = check_permission(
            self.request.user.id, 'Class Routine', 'update')
        if not permission_check:
            return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to retrive End'''
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer_class = ClassRoutineSerializer2
        serializer = serializer_class(
            instance, data=request.data, partial=partial)

        try:
            if serializer.is_valid():
                institution_data = serializer.validated_data.get('institution')
                branch_data = serializer.validated_data.get('branch')
                teacher = serializer.validated_data.get('teacher')
                class_name = serializer.validated_data.get('class_name')
                section = serializer.validated_data.get('section')
                session = serializer.validated_data.get('session')
                version = serializer.validated_data.get('version')
                subject = serializer.validated_data.get('subject')
                class_period = serializer.validated_data.get('class_period')
                day = serializer.validated_data.get('day')
                class_room = serializer.validated_data.get('class_room')
                institution = institution_data if institution_data is not None else self.request.user.institution
                branch = branch_data if branch_data is not None else self.request.user.branch
                routine_count = ClassRoutine.objects.filter(teacher=teacher, class_name=class_name, section=section, session=session, version=version,
                                                            subject=subject, class_period=class_period, day=day, class_room=class_room, institution=institution, branch=branch, status=True).count()
                if (routine_count == 0):
                    # Perform any custom update logic here if needed
                    instance = serializer.save()
                    # Customize the response format for successful update
                    return CustomResponse(code=status.HTTP_200_OK, message="Class Routine updated successfully", data=ClassRoutineSerializer(instance).data)
                return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message=f"This Routine already exits", data=serializer.errors)
            else:
                # Handle validation errors
                return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message="Validation error", data=serializer.errors)
        except Exception as e:
            # Handle other exceptions
            return CustomResponse(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="An error occurred during the update", data=str(e))

class ClassRoutineDelete(generics.UpdateAPIView):
    queryset = ClassRoutine.objects.all()
    serializer_class = ClassRoutineSerializer
    # Requires a valid JWT token for access
    permission_classes = [permissions.IsAuthenticated]

    def partial_update(self, request, *args, **kwargs):
        '''Check user has permission to Delete start'''
        permission_check = check_permission(
            self.request.user.id, 'Class Routine', 'delete')
        if not permission_check:
            return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to Delete End'''
        instance = self.get_object()
        if not instance.status:
            return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message=f"Class Routine already Deleted", data=None)
        # Update the "status" field to False
        instance.status = False
        instance.save()
        # Customize the response format for successful update
        return CustomResponse(code=status.HTTP_200_OK, message=f"Class Routine Delete successfully", data=None)

'''
For Class Routine v2
'''
class ClassRoutineList(generics.ListAPIView):
    serializer_class = ClassRoutineMstListSerializers
    # Requires a valid JWT token for access
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = ClassRoutineMst.objects.filter(status=True).order_by('id')
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

class ClassRoutinev2CreateList(generics.ListCreateAPIView):
    serializer_class = ClassRoutineMstViewSerializers
    # Requires a valid JWT token for access
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = ClassRoutineMst.objects.filter(status=True).order_by('-id')
        try:
            institution_id = self.request.user.institution
            branch_id = self.request.user.branch
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
        '''Check user has permission to View start'''
        permission_check = check_permission(self.request.user.id, 'Class Routine', 'view')
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
        permission_check = check_permission(self.request.user.id, 'Class Routine', 'create')
        if not permission_check:
            return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to View end'''
        serializer_class = ClassRoutineMstCreateSerializers
        serializer = serializer_class(data=request.data)
        try:
            if serializer.is_valid():
                institution_data = serializer.validated_data.get('institution')
                branch_data = serializer.validated_data.get('branch')
                class_name = serializer.validated_data.get('class_name')
                section = serializer.validated_data.get('section')
                session = serializer.validated_data.get('session')
                version = serializer.validated_data.get('version')
                # If data is provided, use it; otherwise, use the values from the request user
                institution = institution_data if institution_data is not None else self.request.user.institution
                branch = branch_data if branch_data is not None else self.request.user.branch
                routine_mst_count = ClassRoutineMst.objects.filter(class_name=class_name,section=section,session=session,version=version,status=True).count()
                if (routine_mst_count==0):
                    instance = serializer.save(institution=institution, branch=branch)
                        # Customize the response data
                    return CustomResponse(code=status.HTTP_200_OK, message="Class Routine created successfully", data=ClassRoutineMstViewSerializers(instance).data)
                else:
                    return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message="Class Routine already exists for this class", data=serializer.errors)
            # If the serializer is not valid, return an error response
            return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message="Validation error", data=serializer.errors)
        except Exception as e:
            # Handle other exceptions
            return CustomResponse(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="An error occurred during the Create", data=str(e))

class ClassRoutinev2Detail(generics.RetrieveUpdateAPIView):
    queryset = ClassRoutineMst.objects.filter(status=True)
    serializer_class = ClassRoutineMstCreateSerializers
    # Requires a valid JWT token for access
    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        '''Check user has permission to retrive start'''
        permission_check = check_permission(
            self.request.user.id, 'Class Routine', 'view')
        if not permission_check:
            return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to retrive End'''
        try:
            instance = self.get_object()
            # Customize the response format for retrieving a single instance
            return CustomResponse(code=status.HTTP_200_OK, message="Success", data=ClassRoutineMstViewSerializers(instance).data)
        except:
            return CustomResponse(code=status.HTTP_404_NOT_FOUND, message="Not Found", data=None)

    def update(self, request, *args, **kwargs):
        '''Check user has permission to update start'''
        permission_check = check_permission(self.request.user.id, 'Class Routine', 'update')
        if not permission_check:
            return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to retrive End'''
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer_class = ClassRoutineMstCreateSerializers
        serializer = serializer_class(instance, data=request.data, partial=partial)
        try:
            if serializer.is_valid():
                institution_data = serializer.validated_data.get('institution')
                branch_data = serializer.validated_data.get('branch')
                class_name = serializer.validated_data.get('class_name')
                section = serializer.validated_data.get('section')
                session = serializer.validated_data.get('session')
                version = serializer.validated_data.get('version')
                institution = institution_data if institution_data is not None else self.request.user.institution
                branch = branch_data if branch_data is not None else self.request.user.branch
                if(class_name==instance.class_name and section==instance.section and session==instance.session and version==instance.version):
                    instance = serializer.save()
                    return CustomResponse(code=status.HTTP_200_OK, message="Class Routine updated successfully", data=ClassRoutineMstViewSerializers(instance).data)
                else:
                    routine_mst_count = ClassRoutineMst.objects.filter(class_name=class_name,section=section,session=session,version=version,status=True).count()
                    if (routine_mst_count == 0):
                        # Perform any custom update logic here if needed
                        instance = serializer.save()
                        # Customize the response format for successful update
                        return CustomResponse(code=status.HTTP_200_OK, message="Class Routine updated successfully", data=ClassRoutineMstViewSerializers(instance).data)
                    return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message=f"This Routine already exits", data=serializer.errors)
            else:
                # Handle validation errors
                return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message="Validation error", data=serializer.errors)
        except Exception as e:
            # Handle other exceptions
            return CustomResponse(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="An error occurred during the update", data=str(e))

class ClassRoutinev2Delete(generics.UpdateAPIView):
    queryset = ClassRoutineMst.objects.all()
    serializer_class = ClassRoutineMstCreateSerializers
    # Requires a valid JWT token for access
    permission_classes = [permissions.IsAuthenticated]

    def partial_update(self, request, *args, **kwargs):
        '''Check user has permission to Delete start'''
        permission_check = check_permission(self.request.user.id, 'Class Routine', 'delete')
        if not permission_check:
            return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to Delete End'''
        instance = self.get_object()
        
        if not instance.status:
            return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message=f"Class Routine already Deleted", data=None)
        # Update the "status" field to False
        instance.status = False
        instance.save()
        for routine_dtl in ClassRoutiineDtl.objects.filter(status=True,class_routine_mst=instance):
            routine_dtl.status = False
            routine_dtl.save()
        # Customize the response format for successful update
        return CustomResponse(code=status.HTTP_200_OK, message=f"Class Routine Delete successfully", data=None)

class ClassRoutineSearch(generics.CreateAPIView):
    serializer_class = ClassRoutineDtlListSerializers
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        version=self.request.data['version']
        session=self.request.data['session']
        class_name=self.request.data['class_name']
        section=self.request.data['section']
        group=self.request.data['group']
        if group:
            queryset = ClassRoutineMst.objects.filter(version=version,session=session,class_name=class_name,section=section,group=group,status=True).order_by('-id')
        else:
            queryset = ClassRoutineMst.objects.filter(version=version,session=session,class_name=class_name,section=section,status=True).order_by('-id')
        try:
            institution_id = self.request.user.institution
            branch_id = self.request.user.branch
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
        return queryset.first().routine_dtl.all() if queryset.exists() else ClassRoutiineDtl.objects.none()

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

class ClassRoutineV2Search(generics.CreateAPIView):
    serializer_class = ClassRoutineMstViewSerializers
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        version=self.request.data['version']
        session=self.request.data['session']
        class_name=self.request.data['class_name']
        section=self.request.data['section']
        group=self.request.data['group']
        if group:
            queryset = ClassRoutineMst.objects.filter(version=version,session=session,class_name=class_name,section=section,group=group,status=True).order_by('-id')
        else:
            queryset = ClassRoutineMst.objects.filter(version=version,session=session,class_name=class_name,section=section,status=True).order_by('-id')
        try:
            institution_id = self.request.user.institution
            branch_id = self.request.user.branch
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

class ClassRoutineDetailsDelete(generics.UpdateAPIView):
    queryset = ClassRoutiineDtl.objects.filter(status=True)
    serializer_class = ClassRoutineDtlDeleteSerializers
    # Requires a valid JWT token for access
    permission_classes = [permissions.IsAuthenticated]

    def partial_update(self, request, *args, **kwargs):
        '''Check user has permission to Delete start'''
        permission_check = check_permission(self.request.user.id, 'Class Routine', 'delete')
        if not permission_check:
            return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to Delete End'''
        instance = self.get_object()
        if not instance.status:
            return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message=f"Routine already Deleted", data=None)
        # Update the "status" field to False
        instance.status = False
        instance.save()
        # Customize the response format for successful update
        return CustomResponse(code=status.HTTP_200_OK, message=f"Routine Delete successfully", data=None)

'''
For Group
'''
class GroupViewCreate(generics.ListAPIView):
    serializer_class = ClassGroupListSerializer
    # Requires a valid JWT token for access
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = ClassGroup.objects.filter(status=True).order_by('id')
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

class GroupListCreate(generics.ListCreateAPIView):
    # queryset = Version.objects.filter(status=True).order_by('id')
    serializer_class = ClassGroupViewSerializer
    # Requires a valid JWT token for access
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = ClassGroup.objects.filter(status=True).order_by('-id')
        try:
            institution_id = self.request.user.institution
            branch_id = self.request.user.branch
            # users = Authentication.objects.get(id=user_id)
            if institution_id and branch_id:
                queryset = queryset.filter(
                    institution=institution_id, branch=branch_id, status=True).order_by('-id')
            elif branch_id:
                queryset = queryset.filter(
                    branch=branch_id, status=True).order_by('-id')
            elif institution_id:
                queryset = queryset.filter(
                    institution=institution_id, status=True).order_by('-id')
            else:
                queryset
        except:
            pass
        return queryset

    def list(self, request, *args, **kwargs):
        '''Check user has permission to View start'''
        permission_check = check_permission(
            self.request.user.id, 'Group', 'view')
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
        permission_check = check_permission(
            self.request.user.id, 'Group', 'create')
        if not permission_check:
            return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to Create End'''
        serializer_class = ClassGroupCreateSerializer
        serializer = serializer_class(data=request.data)
        try:
            if serializer.is_valid():
                institution_data = serializer.validated_data.get('institution')
                branch_data = serializer.validated_data.get('branch')
                name = serializer.validated_data.get('name')
                # If data is provided, use it; otherwise, use the values from the request user
                institution = institution_data if institution_data is not None else self.request.user.institution
                branch = branch_data if branch_data is not None else self.request.user.branch
                group_count = ClassGroup.objects.filter(name__iexact=name, institution=institution, branch=branch, status=True).count()
                if (group_count == 0):
                    instance = serializer.save(institution=institution, branch=branch)
                    # Customize the response data
                    return CustomResponse(code=status.HTTP_200_OK, message="Group created successfully", data=ClassGroupViewSerializer(instance).data)
                return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message=f"Group {name} already exits", data=serializer.errors)
            # If the serializer is not valid, return an error response
            return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message="Validation error", data=serializer.errors)
        except Exception as e:
            # Handle other exceptions
            return CustomResponse(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="An error occurred during the Create", data=str(e))

class GroupUpdateDetail(generics.RetrieveUpdateAPIView):
    queryset = ClassGroup.objects.all()
    serializer_class = ClassGroupCreateSerializer
    # Requires a valid JWT token for access
    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        '''Check user has permission to retrive start'''
        permission_check = check_permission(
            self.request.user.id, 'Group', 'view')
        if not permission_check:
            return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to retrive End'''

        instance = self.get_object()
        # Customize the response format for retrieving a single instance
        return CustomResponse(code=status.HTTP_200_OK, message="Success", data=ClassGroupViewSerializer(instance).data)

    def update(self, request, *args, **kwargs):
        '''Check user has permission to update start'''
        permission_check = check_permission(
            self.request.user.id, 'Version', 'update')
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
                group_count = ClassGroup.objects.filter(name__iexact=name, institution=institution, branch=branch, status=True).count()
                if (group_count == 0):
                    # Perform any custom update logic here if needed
                    instance = serializer.save()
                    # Customize the response data
                    return CustomResponse(code=status.HTTP_200_OK, message="Group Update successfully", data=ClassGroupViewSerializer(instance).data)
                return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message=f"Group {name} already exits", data=serializer.errors)
                # Customize the response format for successful update
            else:
                # Handle validation errors
                return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message="Validation error", data=serializer.errors)
        except Exception as e:
            # Handle other exceptions
            return CustomResponse(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="An error occurred during the update", data=str(e))

class GroupDelete(generics.UpdateAPIView):
    queryset = ClassGroup.objects.all()
    serializer_class = ClassGroupCreateSerializer
    # Requires a valid JWT token for access
    permission_classes = [permissions.IsAuthenticated]

    def partial_update(self, request, *args, **kwargs):
        '''Check user has permission to Delete start'''
        permission_check = check_permission(self.request.user.id, 'Group', 'delete')
        if not permission_check:
            return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to Delete End'''

        instance = self.get_object()
        if not instance.status:
            return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message=f"Group {instance.name} already Deleted", data=None)
        # Update the "status" field to False
        instance.status = False
        instance.save()
        # Customize the response format for successful update
        return CustomResponse(code=status.HTTP_200_OK, message=f"Group {instance.name} Delete successfully", data=None)

'''
For Assign Class Teacher
'''

class ClassTeacherCreateList(generics.ListCreateAPIView):
    # queryset = Version.objects.filter(status=True).order_by('id')
    serializer_class = ClassTeacherViewSerializer
    # Requires a valid JWT token for access
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = ClassTeacher.objects.filter(status=True).order_by('-id')
        try:
            institution_id = self.request.user.institution
            branch_id = self.request.user.branch
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
        '''Check user has permission to View start'''
        permission_check = check_permission(
            self.request.user.id, 'Assign Class Teacher', 'view')
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
        permission_check = check_permission(
            self.request.user.id, 'Assign Class Teacher', 'create')
        if not permission_check:
            return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to View end'''
        serializer_class = ClassTeacherCreateSerializer
        serializer = serializer_class(data=request.data)
        try:
            if serializer.is_valid():
                institution_data = serializer.validated_data.get('institution')
                branch_data = serializer.validated_data.get('branch')
                class_name = serializer.validated_data.get('class_name')
                section = serializer.validated_data.get('section')
                session = serializer.validated_data.get('session')
                group = serializer.validated_data.get('group')
                version = serializer.validated_data.get('version')
                teacher = serializer.validated_data.get('teacher')
                # If data is provided, use it; otherwise, use the values from the request user
                institution = institution_data if institution_data is not None else self.request.user.institution
                branch = branch_data if branch_data is not None else self.request.user.branch
                class_count = ClassTeacher.objects.filter(class_name=class_name,group=group, section=section, session=session, version=version, institution=institution, branch=branch, status=True).count()
                if (class_count==0):
                    class_teacher_count = ClassTeacher.objects.filter(teacher=teacher, session=session, institution=institution, branch=branch, status=True).count()
                    if (class_teacher_count == 0):
                        instance = serializer.save(institution=institution, branch=branch)
                        # Customize the response data
                        return CustomResponse(code=status.HTTP_200_OK, message="Class Teacher Assign successfully", data=ClassTeacherViewSerializer(instance).data)
                    return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message=f"Class Teacher already Assign", data=serializer.errors)
                else:
                    return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message=f"Class already Assign", data=serializer.errors)
            # If the serializer is not valid, return an error response
            return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message="Validation error", data=serializer.errors)
        except Exception as e:
            # Handle other exceptions
            return CustomResponse(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="An error occurred during the Create", data=str(e))

class ClassTeacherDetail(generics.RetrieveUpdateAPIView):
    queryset = ClassTeacher.objects.all()
    serializer_class = ClassTeacherCreateSerializer
    # Requires a valid JWT token for access
    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        '''Check user has permission to View start'''
        permission_check = check_permission(
            self.request.user.id, 'Assign Class Teacher', 'view')
        if not permission_check:
            return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to View end'''
        instance = self.get_object()
        # Customize the response format for retrieving a single instance
        return CustomResponse(code=status.HTTP_200_OK, message="Success", data=ClassTeacherViewSerializer(instance).data)

    def update(self, request, *args, **kwargs):
        '''Check user has permission to View start'''
        permission_check = check_permission(
            self.request.user.id, 'Assign Class Teacher', 'update')
        if not permission_check:
            return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to View end'''
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer_class = ClassTeacherCreateSerializer
        serializer = serializer_class(instance,data=request.data,partial=partial)

        try:
            if serializer.is_valid():
                institution_data = serializer.validated_data.get('institution')
                branch_data = serializer.validated_data.get('branch')
                class_name = serializer.validated_data.get('class_name')
                section = serializer.validated_data.get('section')
                session = serializer.validated_data.get('session')
                version = serializer.validated_data.get('version')
                group = serializer.validated_data.get('group')
                teacher = serializer.validated_data.get('teacher')
                # If data is provided, use it; otherwise, use the values from the request user
                institution = institution_data if institution_data is not None else self.request.user.institution
                branch = branch_data if branch_data is not None else self.request.user.branch
                class_teacher_count = ClassTeacher.objects.filter(teacher=teacher,group=group,class_name=class_name, section=section, session=session, version=version, institution=institution, branch=branch, status=True).count()
                if (class_teacher_count == 0):
                    # Perform any custom update logic here if needed
                    instance = serializer.save()
                    # Customize the response format for successful update
                    return CustomResponse(code=status.HTTP_200_OK, message="Class Teacher updated successfully", data=ClassTeacherViewSerializer(instance).data)
                return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message=f"Class Teacher already exits", data=serializer.errors)
            else:
                # Handle validation errors
                return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message="Validation error", data=serializer.errors)
        except Exception as e:
            # Handle other exceptions
            return CustomResponse(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="An error occurred during the update", data=str(e))

class ClassTeacherDelete(generics.UpdateAPIView):
    queryset = ClassTeacher.objects.all()
    serializer_class = ClassTeacherCreateSerializer
    # Requires a valid JWT token for access
    permission_classes = [permissions.IsAuthenticated]

    def partial_update(self, request, *args, **kwargs):
        '''Check user has permission to View start'''
        permission_check = check_permission(self.request.user.id, 'Assign Class Teacher', 'delete')
        if not permission_check:
            return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to View end'''
        instance = self.get_object()
        if not instance.status:
            return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message=f"Assign Class Teacher already Deleted", data=None)
        # Update the "status" field to False
        instance.status = False
        instance.save()
        # Customize the response format for successful update
        return CustomResponse(code=status.HTTP_200_OK, message=f"Assign Class Teacher Delete successfully", data=None)

'''
For Teacher TimeTable List
'''
class TeacherTimeTableList(generics.ListAPIView):
    serializer_class = ClassRoutineDtlSerializer
    # Requires a valid JWT token for access
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        staff_id = self.kwargs.get('staff_id')  # assuming staff_id is passed as a URL parameter
        return ClassRoutiineDtl.objects.filter(teacher=staff_id,status=True)

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            serializer = self.serializer_class(queryset, many=True)
            # Organize data by days
            timetable_by_days = {}
            for entry in serializer.data:
                day = entry['day']['long_name']
                if day not in timetable_by_days:
                    timetable_by_days[day] = []
                timetable_by_days[day].append({
                    "class_name": entry['class_routine_mst']['class_name'],
                    "section": entry['class_routine_mst']['section'],
                    "group": entry['class_routine_mst']['group'],
                    "class_period": entry['class_period'],
                    "subject": entry['subject'],
                    "class_room": entry['class_room'],
                })
                response_data = {
                    "message": "Success",
                    "data": timetable_by_days,
                }
            return CustomResponse(code=status.HTTP_200_OK,data=timetable_by_days, status=status.HTTP_200_OK)
        except:
            return CustomResponse(code=status.HTTP_404_NOT_FOUND, message="Not Found", data=None)


'''
For Student Time 
'''
class StudentTimeTable(generics.ListAPIView):
    serializer_class = ClassRoutineDtlSerializer
    # Requires a valid JWT token for access
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        username = self.request.user
        model_name = self.request.user.model_name
        institution = self.request.user.institution
        branch = self.request.user.branch
        try:
            std_info = Student.objects.get(student_no=username,status=True)
            enroll = StudentEnroll.objects.filter(is_active=True,status=True,student=std_info).last()
            if enroll:
                roll = enroll.roll
                version = enroll.version
                session = enroll.session
                section= enroll.section
                class_name = enroll.class_name
                group= enroll.group

                if group:
                    class_mst = ClassRoutineMst.objects.get(status=True,institution=institution,branch=branch,version=version,session=session,section=section,class_name=class_name,group=group)
                else:
                    class_mst = ClassRoutineMst.objects.get(status=True,institution=institution,branch=branch,version=version,session=session,section=section,class_name=class_name)       

            return ClassRoutiineDtl.objects.filter(class_routine_mst=class_mst,status=True)
        except:
            pass
    
    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            serializer = self.serializer_class(queryset, many=True)
            # Organize data by days
            timetable_by_days = {}
            for entry in serializer.data:
                day = entry['day']['long_name']
                if day not in timetable_by_days:
                    timetable_by_days[day] = []
                timetable_by_days[day].append({
                    # "class_name": entry['class_routine_mst']['class_name'],
                    # "section": entry['class_routine_mst']['section'],
                    # "group": entry['class_routine_mst']['group'],
                    "class_period": entry['class_period'],
                    "subject": entry['subject'],
                    "class_room": entry['class_room'],
                    "teacher": entry['teacher'],
                })
                response_data = {
                    "message": "Success",
                    "data": timetable_by_days,
                }
            return CustomResponse(code=status.HTTP_200_OK,data=timetable_by_days, status=status.HTTP_200_OK)
        except:
            return CustomResponse(code=status.HTTP_404_NOT_FOUND, message="Not Found", data=None)


class StudentTextBookList(generics.ListAPIView):
    serializer_class = ClassSubjectStdViewSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        user = self.request.user
        institution = user.institution
        branch = user.branch

        queryset = ClassSubject.objects.filter(status=True, institution=institution, branch=branch)

        try:
            student = Student.objects.get(student_no=user, status=True)
            enroll = StudentEnroll.objects.filter(is_active=True, status=True, student=student).last()
            
            if enroll:
                filters = {
                    "status": True,
                    "institution": institution,
                    "branch": branch,
                    "version": enroll.version,
                    "session": enroll.session,
                    "section": enroll.section,
                    "class_name": enroll.class_name,
                }

                if enroll.group:
                    filters["group"] = enroll.group
                    queryset = ClassSubject.objects.filter(**filters)
                else:
                    queryset = ClassSubject.objects.filter(**filters)
                    print(filters,'++++++++++++++',queryset)
        except Student.DoesNotExist:
            pass

        return queryset

    def list(self, request, *args, **kwargs):
        # Check user has permission to view "My Subject"
        if not check_permission(self.request.user.id, "My Subject", "view"):
            return Response({
                "code": status.HTTP_401_UNAUTHORIZED,
                "message": "Permission denied",
                "data": None
            })

        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "code": 200,
            "message": "Success",
            "data": serializer.data,
            "pagination": {
                "next": None,
                "previous": None,
                "count": queryset.count(),
            },
        })