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


class ReligionList(generics.ListAPIView):
    serializer_class = ReligionSerializer
    # Requires a valid JWT token for access
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = Religion.objects.filter(status=True).order_by('-id')
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

class BloodGroupList(generics.ListAPIView):
    serializer_class = BloodGroupSerializer
    # Requires a valid JWT token for access
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = BloodGroup.objects.filter(status=True).order_by('name')
        try:
            institution_id = self.request.user.institution
            branch_id = self.request.user.branch
            # users = Authentication.objects.get(id=user_id)
            if institution_id and branch_id:
                queryset = queryset.filter(
                    institution=institution_id, branch=branch_id, status=True).order_by('name')
            elif branch_id:
                queryset = queryset.filter(
                    branch=branch_id, status=True).order_by('name')
            elif institution_id:
                queryset = queryset.filter(
                    institution=institution_id, status=True).order_by('name')
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

class GenderList(generics.ListAPIView):
    serializer_class = GenderSerializer
    # Requires a valid JWT token for access
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = Gender.objects.filter(status=True).order_by('name')
        try:
            institution_id = self.request.user.institution
            branch_id = self.request.user.branch
            # users = Authentication.objects.get(id=user_id)
            if institution_id and branch_id:
                queryset = queryset.filter(
                    institution=institution_id, branch=branch_id, status=True).order_by('name')
            elif branch_id:
                queryset = queryset.filter(
                    branch=branch_id, status=True).order_by('name')
            elif institution_id:
                queryset = queryset.filter(
                    institution=institution_id, status=True).order_by('name')
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

class OccupationList(generics.ListAPIView):
    serializer_class = OccupationSerializer
    # Requires a valid JWT token for access
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = Occupation.objects.filter(status=True).order_by('name')
        try:
            institution_id = self.request.user.institution
            branch_id = self.request.user.branch
            # users = Authentication.objects.get(id=user_id)
            if institution_id and branch_id:
                queryset = queryset.filter(
                    institution=institution_id, branch=branch_id, status=True).order_by('name')
            elif branch_id:
                queryset = queryset.filter(
                    branch=branch_id, status=True).order_by('name')
            elif institution_id:
                queryset = queryset.filter(
                    institution=institution_id, status=True).order_by('name')
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

class RelationList(generics.ListAPIView):
    serializer_class = RelationSerializer
    # Requires a valid JWT token for access
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = Relation.objects.filter(status=True).order_by('name')
        try:
            institution_id = self.request.user.institution
            branch_id = self.request.user.branch
            # users = Authentication.objects.get(id=user_id)
            if institution_id and branch_id:
                queryset = queryset.filter(
                    institution=institution_id, branch=branch_id, status=True).order_by('name')
            elif branch_id:
                queryset = queryset.filter(
                    branch=branch_id, status=True).order_by('name')
            elif institution_id:
                queryset = queryset.filter(
                    institution=institution_id, status=True).order_by('name')
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

class FloorList(generics.ListAPIView):
    serializer_class = FloorTypeSerializer
    # Requires a valid JWT token for access
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = FloorType.objects.filter(status=True).order_by('sl_no')
        try:
            institution_id = self.request.user.institution
            branch_id = self.request.user.branch
            # users = Authentication.objects.get(id=user_id)
            if institution_id and branch_id:
                queryset = queryset.filter(
                    institution=institution_id, branch=branch_id, status=True).order_by('sl_no')
            elif branch_id:
                queryset = queryset.filter(
                    branch=branch_id, status=True).order_by('sl_no')
            elif institution_id:
                queryset = queryset.filter(
                    institution=institution_id, status=True).order_by('sl_no')
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

class SubjectTypeList(generics.ListAPIView):
    serializer_class = SubjectTypeSerializer
    # Requires a valid JWT token for access
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = SubjectType.objects.filter(status=True).order_by('id')
        # try:
        #     institution_id = self.request.user.institution
        #     branch_id = self.request.user.branch
        #     # users = Authentication.objects.get(id=user_id)
        #     if institution_id and branch_id:
        #         queryset = queryset.filter(institution=institution_id, branch=branch_id,status=True).order_by('sl_no')
        #     elif branch_id:
        #         queryset = queryset.filter(branch=branch_id,status=True).order_by('sl_no')
        #     elif institution_id:
        #         queryset = queryset.filter(institution=institution_id,status=True).order_by('sl_no')
        #     else:
        #         queryset
        # except:
        #     pass
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

class RoleList(generics.ListAPIView):
    serializer_class = RoleSerializer
    # Requires a valid JWT token for access
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = Role.objects.filter(status=True).order_by('id')
        # try:
        #     institution_id = self.request.user.institution
        #     branch_id = self.request.user.branch
        #     # users = Authentication.objects.get(id=user_id)
        #     if institution_id and branch_id:
        #         queryset = queryset.filter(institution=institution_id, branch=branch_id,status=True).order_by('sl_no')
        #     elif branch_id:
        #         queryset = queryset.filter(branch=branch_id,status=True).order_by('sl_no')
        #     elif institution_id:
        #         queryset = queryset.filter(institution=institution_id,status=True).order_by('sl_no')
        #     else:
        #         queryset
        # except:
        #     pass
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

class RoleList(generics.ListAPIView):
    serializer_class = RoleSerializer
    # Requires a valid JWT token for access
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = Role.objects.filter(status=True).order_by('id')
        # try:
        #     institution_id = self.request.user.institution
        #     branch_id = self.request.user.branch
        #     # users = Authentication.objects.get(id=user_id)
        #     if institution_id and branch_id:
        #         queryset = queryset.filter(institution=institution_id, branch=branch_id,status=True).order_by('sl_no')
        #     elif branch_id:
        #         queryset = queryset.filter(branch=branch_id,status=True).order_by('sl_no')
        #     elif institution_id:
        #         queryset = queryset.filter(institution=institution_id,status=True).order_by('sl_no')
        #     else:
        #         queryset
        # except:
        #     pass
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

class MaritalStatusList(generics.ListAPIView):
    serializer_class = MaritalStatusViewSerializer
    # Requires a valid JWT token for access
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = MaritalStatus.objects.filter(status=True).order_by('id')
        # try:
        #     institution_id = self.request.user.institution
        #     branch_id = self.request.user.branch
        #     # users = Authentication.objects.get(id=user_id)
        #     if institution_id and branch_id:
        #         queryset = queryset.filter(institution=institution_id, branch=branch_id,status=True).order_by('sl_no')
        #     elif branch_id:
        #         queryset = queryset.filter(branch=branch_id,status=True).order_by('sl_no')
        #     elif institution_id:
        #         queryset = queryset.filter(institution=institution_id,status=True).order_by('sl_no')
        #     else:
        #         queryset
        # except:
        #     pass
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

class AttendancetypeList(generics.ListAPIView):
    serializer_class = AttendanceTypeViewSerializer
    # Requires a valid JWT token for access
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = AttendanceType.objects.filter(status=True,display=True).order_by('ordering','id')
        # try:
        #     institution_id = self.request.user.institution
        #     branch_id = self.request.user.branch
        #     # users = Authentication.objects.get(id=user_id)
        #     if institution_id and branch_id:
        #         queryset = queryset.filter(institution=institution_id, branch=branch_id,status=True).order_by('sl_no')
        #     elif branch_id:
        #         queryset = queryset.filter(branch=branch_id,status=True).order_by('sl_no')
        #     elif institution_id:
        #         queryset = queryset.filter(institution=institution_id,status=True).order_by('sl_no')
        #     else:
        #         queryset
        # except:
        #     pass
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

class HolidayTypeList(generics.ListAPIView):
    serializer_class = HolidayTypeViewSerializer
    # Requires a valid JWT token for access
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = HolidayType.objects.filter(status=True).order_by('id')
        # try:
        #     institution_id = self.request.user.institution
        #     branch_id = self.request.user.branch
        #     # users = Authentication.objects.get(id=user_id)
        #     if institution_id and branch_id:
        #         queryset = queryset.filter(institution=institution_id, branch=branch_id,status=True).order_by('sl_no')
        #     elif branch_id:
        #         queryset = queryset.filter(branch=branch_id,status=True).order_by('sl_no')
        #     elif institution_id:
        #         queryset = queryset.filter(institution=institution_id,status=True).order_by('sl_no')
        #     else:
        #         queryset
        # except:
        #     pass
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

'''
For Education Board
'''

class EduBoardList(generics.ListAPIView):
    serializer_class = EducationBoardViewSerializer
    # Requires a valid JWT token for access
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = EducationBoard.objects.filter(status=True).order_by('-id')
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

class BoardCreateList(generics.ListCreateAPIView):
    # queryset = Version.objects.filter(status=True).order_by('id')
    serializer_class = EducationBoardSerializer
    # Requires a valid JWT token for access
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = EducationBoard.objects.filter(status=True).order_by('-id')
        return queryset

    def list(self, request, *args, **kwargs):
        '''Check user has permission to View start'''
        permission_check = check_permission(
            self.request.user.id, 'Board', 'view')
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
            self.request.user.id, 'Board', 'create')
        if not permission_check:
            return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to Create End'''

        serializer = self.get_serializer(data=request.data)
        try:
            if serializer.is_valid():
                name = serializer.validated_data.get('name')
                # If data is provided, use it; otherwise, use the values from the request user
                board_count = EducationBoard.objects.filter(
                    name__iexact=name, status=True).count()
                if (board_count == 0):
                    instance = serializer.save()
                    # Customize the response data
                    return CustomResponse(code=status.HTTP_200_OK, message="Board created successfully", data=EducationBoardSerializer(instance).data)
                return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message=f"Board {name} already exits", data=serializer.errors)
            # If the serializer is not valid, return an error response
            return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message="Validation error", data=serializer.errors)
        except Exception as e:
            # Handle other exceptions
            return CustomResponse(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="An error occurred during the Create", data=str(e))

class BoardDetail(generics.RetrieveUpdateAPIView):
    queryset = EducationBoard.objects.all()
    serializer_class = EducationBoardSerializer
    # Requires a valid JWT token for access
    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        '''Check user has permission to retrive start'''
        permission_check = check_permission(
            self.request.user.id, 'Board', 'view')
        if not permission_check:
            return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to retrive End'''

        instance = self.get_object()
        # Customize the response format for retrieving a single instance
        return CustomResponse(code=status.HTTP_200_OK, message="Success", data=EducationBoardSerializer(instance).data)

    def update(self, request, *args, **kwargs):
        '''Check user has permission to update start'''
        permission_check = check_permission(
            self.request.user.id, 'Board', 'update')
        if not permission_check:
            return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to retrive End'''

        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)

        try:
            if serializer.is_valid():
                name = serializer.validated_data.get('name')
                # If data is provided, use it; otherwise, use the values from the request user
                board_count = EducationBoard.objects.filter(
                    name__iexact=name, status=True).count()
                if (board_count == 0):
                    # Perform any custom update logic here if needed
                    instance = serializer.save()
                    # Customize the response data
                    return CustomResponse(code=status.HTTP_200_OK, message="Board update successfully", data=EducationBoardSerializer(instance).data)
                return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message=f"Board {name} already exits", data=serializer.errors)
                # Customize the response format for successful update
            else:
                # Handle validation errors
                return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message="Validation error", data=serializer.errors)
        except Exception as e:
            # Handle other exceptions
            return CustomResponse(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="An error occurred during the update", data=str(e))

class BoardDelete(generics.UpdateAPIView):
    queryset = EducationBoard.objects.all()
    serializer_class = EducationBoardSerializer
    # Requires a valid JWT token for access
    permission_classes = [permissions.IsAuthenticated]

    def partial_update(self, request, *args, **kwargs):
        '''Check user has permission to Delete start'''
        permission_check = check_permission(
            self.request.user.id, 'Board', 'delete')
        if not permission_check:
            return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to Delete End'''

        instance = self.get_object()
        if not instance.status:
            return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message=f"Board {instance.name} already Deleted", data=None)
        # Update the "status" field to False
        instance.status = False
        instance.save()
        # Customize the response format for successful update
        return CustomResponse(code=status.HTTP_200_OK, message=f"Board {instance.name} Delete successfully", data=None)

'''
For District
'''

class DistrictList(generics.ListAPIView):
    serializer_class = DistrictdViewSerializer
    # Requires a valid JWT token for access
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = District.objects.filter(status=True).order_by('-id')
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

class DistrictCreateList(generics.ListCreateAPIView):
    # queryset = Version.objects.filter(status=True).order_by('id')
    serializer_class = DistrictSerializer
    # Requires a valid JWT token for access
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = District.objects.filter(status=True).order_by('-id')
        return queryset

    def list(self, request, *args, **kwargs):
        '''Check user has permission to View start'''
        permission_check = check_permission(
            self.request.user.id, 'District', 'view')
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
            self.request.user.id, 'District', 'create')
        if not permission_check:
            return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to Create End'''
        serializer_class = DistrictCreateSerializer
        serializer = serializer_class(data=request.data)
        # serializer = self.get_serializer(data=request.data)
        try:
            if serializer.is_valid():
                name = serializer.validated_data.get('name')
                division = serializer.validated_data.get('division')
                # If data is provided, use it; otherwise, use the values from the request user
                district_count = District.objects.filter(
                    name__iexact=name, division=division, status=True).count()
                if (district_count == 0):
                    instance = serializer.save()
                    # Customize the response data
                    return CustomResponse(code=status.HTTP_200_OK, message="District created successfully", data=DistrictSerializer(instance).data)
                return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message=f"District {name} already exits", data=serializer.errors)
            # If the serializer is not valid, return an error response
            return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message="Validation error", data=serializer.errors)
        except Exception as e:
            # Handle other exceptions
            return CustomResponse(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="An error occurred during the Create", data=str(e))

class DistrictDetail(generics.RetrieveUpdateAPIView):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer
    # Requires a valid JWT token for access
    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        '''Check user has permission to retrive start'''
        permission_check = check_permission(
            self.request.user.id, 'District', 'view')
        if not permission_check:
            return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to retrive End'''

        instance = self.get_object()
        # Customize the response format for retrieving a single instance
        return CustomResponse(code=status.HTTP_200_OK, message="Success", data=DistrictSerializer(instance).data)

    def update(self, request, *args, **kwargs):
        '''Check user has permission to update start'''
        permission_check = check_permission(
            self.request.user.id, 'District', 'update')
        if not permission_check:
            return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to retrive End'''

        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer_class = DistrictCreateSerializer
        serializer = serializer_class(
            instance, data=request.data, partial=partial)

        try:
            if serializer.is_valid():
                name = serializer.validated_data.get('name')
                division = serializer.validated_data.get('division')
                # If data is provided, use it; otherwise, use the values from the request user
                district_count = District.objects.filter(
                    name__iexact=name, division=division, status=True).count()
                if (district_count == 0):
                    # Perform any custom update logic here if needed
                    instance = serializer.save()
                    # Customize the response data
                    return CustomResponse(code=status.HTTP_200_OK, message="District update successfully", data=DistrictSerializer(instance).data)
                return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message=f"District {name} already exits", data=serializer.errors)
                # Customize the response format for successful update
            else:
                # Handle validation errors
                return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message="Validation error", data=serializer.errors)
        except Exception as e:
            # Handle other exceptions
            return CustomResponse(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="An error occurred during the update", data=str(e))

class DistrictDelete(generics.UpdateAPIView):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer
    # Requires a valid JWT token for access
    permission_classes = [permissions.IsAuthenticated]

    def partial_update(self, request, *args, **kwargs):
        '''Check user has permission to Delete start'''
        permission_check = check_permission(
            self.request.user.id, 'District', 'delete')
        if not permission_check:
            return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to Delete End'''

        instance = self.get_object()
        if not instance.status:
            return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message=f"District {instance.name} already Deleted", data=None)
        # Update the "status" field to False
        instance.status = False
        instance.save()
        # Customize the response format for successful update
        return CustomResponse(code=status.HTTP_200_OK, message=f"District {instance.name} Delete successfully", data=None)

'''
For Division
'''

class DivisionList(generics.ListAPIView):
    serializer_class = DivisionViewSerializer
    # Requires a valid JWT token for access
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = Division.objects.filter(status=True).order_by('-id')
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

class DivisionCreateList(generics.ListCreateAPIView):
    # queryset = Version.objects.filter(status=True).order_by('id')
    serializer_class = DivisionSerializer
    # Requires a valid JWT token for access
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = Division.objects.filter(status=True).order_by('-id')
        return queryset

    def list(self, request, *args, **kwargs):
        '''Check user has permission to View start'''
        permission_check = check_permission(
            self.request.user.id, 'Division', 'view')
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
            self.request.user.id, 'Division', 'create')
        if not permission_check:
            return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to View end'''
        serializer_class = DivisionCreateSerializer
        serializer = serializer_class(data=request.data)
        try:
            if serializer.is_valid():
                name = serializer.validated_data.get('name')
                country = serializer.validated_data.get('country')
                # If data is provided, use it; otherwise, use the values from the request user
                division_count = Division.objects.filter(
                    name__iexact=name, country=country, status=True).count()
                if (division_count == 0):
                    instance = serializer.save()
                    # Customize the response data
                    return CustomResponse(code=status.HTTP_200_OK, message="Division created successfully", data=DivisionSerializer(instance).data)
                return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message=f"Division already exits", data=serializer.errors)
            # If the serializer is not valid, return an error response
            return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message="Validation error", data=serializer.errors)
        except Exception as e:
            # Handle other exceptions
            return CustomResponse(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="An error occurred during the Create", data=str(e))

class DivisionDetail(generics.RetrieveUpdateAPIView):
    queryset = Division.objects.all()
    serializer_class = DivisionSerializer
    # Requires a valid JWT token for access
    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        '''Check user has permission to View start'''
        permission_check = check_permission(
            self.request.user.id, 'Division', 'view')
        if not permission_check:
            return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to View end'''
        instance = self.get_object()
        # Customize the response format for retrieving a single instance
        return CustomResponse(code=status.HTTP_200_OK, message="Success", data=DivisionSerializer(instance).data)

    def update(self, request, *args, **kwargs):
        '''Check user has permission to View start'''
        permission_check = check_permission(
            self.request.user.id, 'Division', 'update')
        if not permission_check:
            return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to View end'''
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer_class = DivisionCreateSerializer
        serializer = serializer_class(
            instance, data=request.data, partial=partial)

        try:
            if serializer.is_valid():
                name = serializer.validated_data.get('name')
                country = serializer.validated_data.get('country')
                # If data is provided, use it; otherwise, use the values from the request user
                division_count = Division.objects.filter(
                    name__iexact=name, country=country, status=True).count()
                if (division_count == 0):
                    # Perform any custom update logic here if needed
                    instance = serializer.save()
                    # Customize the response format for successful update
                    return CustomResponse(code=status.HTTP_200_OK, message="Division updated successfully", data=DivisionSerializer(instance).data)
                return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message=f"Division already exits", data=serializer.errors)
            else:
                # Handle validation errors
                return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message="Validation error", data=serializer.errors)
        except Exception as e:
            # Handle other exceptions
            return CustomResponse(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="An error occurred during the update", data=str(e))

class DivisionDelete(generics.UpdateAPIView):
    queryset = Division.objects.all()
    serializer_class = DivisionSerializer
    # Requires a valid JWT token for access
    permission_classes = [permissions.IsAuthenticated]

    def partial_update(self, request, *args, **kwargs):
        '''Check user has permission to View start'''
        permission_check = check_permission(
            self.request.user.id, 'Division', 'delete')
        if not permission_check:
            return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to View end'''
        instance = self.get_object()
        if not instance.status:
            return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message=f"Division {instance.name} already Deleted", data=None)
        # Update the "status" field to False
        instance.status = False
        instance.save()
        # Customize the response format for successful update
        return CustomResponse(code=status.HTTP_200_OK, message=f"Division {instance.name} Delete successfully", data=None)

'''
For Country
'''

class CountryList(generics.ListAPIView):
    serializer_class = CountryViewSerializer
    # Requires a valid JWT token for access
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = Country.objects.filter(status=True).order_by('-id')
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

class CountryCreateList(generics.ListCreateAPIView):
    # queryset = Version.objects.filter(status=True).order_by('id')
    serializer_class = CountrySerializer
    # Requires a valid JWT token for access
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = Country.objects.filter(status=True).order_by('-id')
        return queryset

    def list(self, request, *args, **kwargs):
        '''Check user has permission to View start'''
        permission_check = check_permission(
            self.request.user.id, 'Country', 'view')
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
            self.request.user.id, 'Country', 'create')
        if not permission_check:
            return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to Create End'''

        serializer = self.get_serializer(data=request.data)
        try:
            if serializer.is_valid():
                name = serializer.validated_data.get('name')
                # If data is provided, use it; otherwise, use the values from the request user
                country_count = Country.objects.filter(
                    name__iexact=name, status=True).count()
                if (country_count == 0):
                    instance = serializer.save()
                    # Customize the response data
                    return CustomResponse(code=status.HTTP_200_OK, message="Country created successfully", data=CountrySerializer(instance).data)
                return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message=f"Country {name} already exits", data=serializer.errors)
            # If the serializer is not valid, return an error response
            return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message="Validation error", data=serializer.errors)
        except Exception as e:
            # Handle other exceptions
            return CustomResponse(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="An error occurred during the Create", data=str(e))

class CountryDetail(generics.RetrieveUpdateAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    # Requires a valid JWT token for access
    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        '''Check user has permission to retrive start'''
        permission_check = check_permission(
            self.request.user.id, 'Country', 'view')
        if not permission_check:
            return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to retrive End'''

        instance = self.get_object()
        # Customize the response format for retrieving a single instance
        return CustomResponse(code=status.HTTP_200_OK, message="Success", data=CountrySerializer(instance).data)

    def update(self, request, *args, **kwargs):
        '''Check user has permission to update start'''
        permission_check = check_permission(
            self.request.user.id, 'Country', 'update')
        if not permission_check:
            return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to retrive End'''

        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)

        try:
            if serializer.is_valid():
                name = serializer.validated_data.get('name')
                # If data is provided, use it; otherwise, use the values from the request user
                country_count = Country.objects.filter(
                    name__iexact=name, status=True).count()
                if (country_count == 0):
                    # Perform any custom update logic here if needed
                    instance = serializer.save()
                    # Customize the response data
                    return CustomResponse(code=status.HTTP_200_OK, message="Country update successfully", data=CountrySerializer(instance).data)
                return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message=f"Country {name} already exits", data=serializer.errors)
                # Customize the response format for successful update
            else:
                # Handle validation errors
                return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message="Validation error", data=serializer.errors)
        except Exception as e:
            # Handle other exceptions
            return CustomResponse(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="An error occurred during the update", data=str(e))

class CountryDelete(generics.UpdateAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    # Requires a valid JWT token for access
    permission_classes = [permissions.IsAuthenticated]

    def partial_update(self, request, *args, **kwargs):
        '''Check user has permission to Delete start'''
        permission_check = check_permission(
            self.request.user.id, 'Country', 'delete')
        if not permission_check:
            return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to Delete End'''

        instance = self.get_object()
        if not instance.status:
            return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message=f"Country {instance.name} already Deleted", data=None)
        # Update the "status" field to False
        instance.status = False
        instance.save()
        # Customize the response format for successful update
        return CustomResponse(code=status.HTTP_200_OK, message=f"Country {instance.name} Delete successfully", data=None)

'''
For Thana
'''

class ThanaList(generics.ListAPIView):
    serializer_class = ThanaViewSerializer
    # Requires a valid JWT token for access
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = Thana.objects.filter(status=True).order_by('-id')
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

class ThanaCreateList(generics.ListCreateAPIView):
    # queryset = Version.objects.filter(status=True).order_by('id')
    serializer_class = ThanaSerializer
    # Requires a valid JWT token for access
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = Thana.objects.filter(status=True).order_by('-id')
        return queryset

    def list(self, request, *args, **kwargs):
        '''Check user has permission to View start'''
        permission_check = check_permission(
            self.request.user.id, 'Thana', 'view')
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
            self.request.user.id, 'Thana', 'create')
        if not permission_check:
            return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to Create End'''
        serializer_class = ThanaCreateSerializer
        serializer = serializer_class(data=request.data)
        try:
            if serializer.is_valid():
                name = serializer.validated_data.get('name')
                district = serializer.validated_data.get('district')
                # If data is provided, use it; otherwise, use the values from the request user
                thana_count = Thana.objects.filter(
                    name__iexact=name, district=district, status=True).count()
                if (thana_count == 0):
                    instance = serializer.save()
                    # Customize the response data
                    return CustomResponse(code=status.HTTP_200_OK, message="Thana created successfully", data=ThanaSerializer(instance).data)
                return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message=f"Thana {name} already exits", data=serializer.errors)
            # If the serializer is not valid, return an error response
            return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message="Validation error", data=serializer.errors)
        except Exception as e:
            # Handle other exceptions
            return CustomResponse(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="An error occurred during the Create", data=str(e))

class ThanaDetail(generics.RetrieveUpdateAPIView):
    queryset = Thana.objects.all()
    serializer_class = ThanaSerializer
    # Requires a valid JWT token for access
    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        '''Check user has permission to retrive start'''
        permission_check = check_permission(
            self.request.user.id, 'Thana', 'view')
        if not permission_check:
            return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to retrive End'''

        instance = self.get_object()
        # Customize the response format for retrieving a single instance
        return CustomResponse(code=status.HTTP_200_OK, message="Success", data=ThanaSerializer(instance).data)

    def update(self, request, *args, **kwargs):
        '''Check user has permission to update start'''
        permission_check = check_permission(
            self.request.user.id, 'Thana', 'update')
        if not permission_check:
            return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to retrive End'''

        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer_class = ThanaCreateSerializer
        serializer = serializer_class(
            instance, data=request.data, partial=partial)

        try:
            if serializer.is_valid():
                name = serializer.validated_data.get('name')
                district = serializer.validated_data.get('district')
                # If data is provided, use it; otherwise, use the values from the request user
                thana_count = Thana.objects.filter(
                    name__iexact=name, district=district, status=True).count()
                if (thana_count == 0):
                    # Perform any custom update logic here if needed
                    instance = serializer.save()
                    # Customize the response data
                    return CustomResponse(code=status.HTTP_200_OK, message="Thana update successfully", data=ThanaSerializer(instance).data)
                return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message=f"Thana {name} already exits", data=serializer.errors)
                # Customize the response format for successful update
            else:
                # Handle validation errors
                return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message="Validation error", data=serializer.errors)
        except Exception as e:
            # Handle other exceptions
            return CustomResponse(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="An error occurred during the update", data=str(e))

class ThanaDelete(generics.UpdateAPIView):
    queryset = Thana.objects.all()
    serializer_class = ThanaSerializer
    # Requires a valid JWT token for access
    permission_classes = [permissions.IsAuthenticated]

    def partial_update(self, request, *args, **kwargs):
        '''Check user has permission to Delete start'''
        permission_check = check_permission(
            self.request.user.id, 'Thana', 'delete')
        if not permission_check:
            return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to Delete End'''

        instance = self.get_object()
        if not instance.status:
            return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message=f"Thana {instance.name} already Deleted", data=None)
        # Update the "status" field to False
        instance.status = False
        instance.save()
        # Customize the response format for successful update
        return CustomResponse(code=status.HTTP_200_OK, message=f"Thana {instance.name} Delete successfully", data=None)

'''
For Contract Type
'''

class ContractTypeList(generics.ListAPIView):
    serializer_class = ContractTypeViewSerializer
    # Requires a valid JWT token for access
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = ContractType.objects.filter(status=True).order_by('-id')
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

'''For Days'''

class DayList(generics.ListAPIView):
    serializer_class = DaySerializer
    # Requires a valid JWT token for access
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = Days.objects.filter(status=True,week_end=False).order_by('sl_no')
        try:
            institution_id = self.request.user.institution
            branch_id = self.request.user.branch
            # users = Authentication.objects.get(id=user_id)
            if institution_id and branch_id:
                queryset = queryset.filter(
                    institution=institution_id, branch=branch_id, status=True).order_by('sl_no')
            elif branch_id:
                queryset = queryset.filter(
                    branch=branch_id, status=True).order_by('sl_no')
            elif institution_id:
                queryset = queryset.filter(
                    institution=institution_id, status=True).order_by('sl_no')
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

class DayCreateList(generics.ListCreateAPIView):
    # queryset = Version.objects.filter(status=True).order_by('id')
    serializer_class = DayCreateSerializer
    # Requires a valid JWT token for access
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = Days.objects.filter(status=True).order_by('sl_no')
        return queryset

    def list(self, request, *args, **kwargs):
        '''Check user has permission to View start'''
        permission_check = check_permission(
            self.request.user.id, 'Day', 'view')
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
        permission_check = check_permission(self.request.user.id, 'Day', 'create')
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
                short_name = serializer.validated_data.get('short_name')
                long_name = serializer.validated_data.get('long_name')
                # If data is provided, use it; otherwise, use the values from the request user
                day_count = Days.objects.filter(long_name__iexact=long_name, status=True).count()
                if (day_count == 0):
                    instance = serializer.save(institution=institution,branch=branch)
                    # Customize the response data
                    return CustomResponse(code=status.HTTP_200_OK, message="Day created successfully", data=DayCreateSerializer(instance).data)
                return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message=f"Day {long_name} already exits", data=serializer.errors)
            # If the serializer is not valid, return an error response
            return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message="Validation error", data=serializer.errors)
        except Exception as e:
            # Handle other exceptions
            return CustomResponse(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="An error occurred during the Create", data=str(e))

class DayDetail(generics.RetrieveUpdateAPIView):
    queryset = Days.objects.all()
    serializer_class = DayCreateSerializer
    # Requires a valid JWT token for access
    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        '''Check user has permission to retrive start'''
        permission_check = check_permission(
            self.request.user.id, 'Day', 'view')
        if not permission_check:
            return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to retrive End'''

        instance = self.get_object()
        # Customize the response format for retrieving a single instance
        return CustomResponse(code=status.HTTP_200_OK, message="Success", data=DayCreateSerializer(instance).data)

    def update(self, request, *args, **kwargs):
        '''Check user has permission to update start'''
        permission_check = check_permission(
            self.request.user.id, 'Day', 'update')
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
                short_name = serializer.validated_data.get('short_name')
                long_name = serializer.validated_data.get('long_name')
                if (long_name==instance.long_name):
                    instance = serializer.save()
                    return CustomResponse(code=status.HTTP_200_OK, message="Day update successfully", data=DayCreateSerializer(instance).data)
                else:
                    
                    institution = institution_data if institution_data is not None else self.request.user.institution
                    branch = branch_data if branch_data is not None else self.request.user.branch
                    # If data is provided, use it; otherwise, use the values from the request user
                    day_count = Days.objects.filter(long_name__iexact=long_name, status=True,institution=institution,branch=branch).count()
                    if (day_count == 0):
                        # Perform any custom update logic here if needed
                        instance = serializer.save()
                        # Customize the response data
                        return CustomResponse(code=status.HTTP_200_OK, message="Day update successfully", data=DayCreateSerializer(instance).data)
                    return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message=f"Day {long_name} already exits", data=serializer.errors)
            else:
                # Handle validation errors
                return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message="Validation error", data=serializer.errors)
        except Exception as e:
            # Handle other exceptions
            return CustomResponse(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="An error occurred during the update", data=str(e))

class DayDelete(generics.UpdateAPIView):
    queryset = Days.objects.all()
    serializer_class = DayCreateSerializer
    # Requires a valid JWT token for access
    permission_classes = [permissions.IsAuthenticated]

    def partial_update(self, request, *args, **kwargs):
        '''Check user has permission to Delete start'''
        permission_check = check_permission(
            self.request.user.id, 'Day', 'delete')
        if not permission_check:
            return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to Delete End'''

        instance = self.get_object()
        if not instance.status:
            return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message=f"Day {instance.long_name} already Deleted", data=None)
        # Update the "status" field to False
        instance.status = False
        instance.save()
        # Customize the response format for successful update
        return CustomResponse(code=status.HTTP_200_OK, message=f"Day {instance.long_name} Delete successfully", data=None)

class PayMethodList(generics.ListAPIView):
    serializer_class = PaymentMethodViewSerializer
    # Requires a valid JWT token for access
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = PaymentMethod.objects.filter(status=True).order_by('id')
        # try:
        #     institution_id = self.request.user.institution
        #     branch_id = self.request.user.branch
        #     # users = Authentication.objects.get(id=user_id)
        #     if institution_id and branch_id:
        #         queryset = queryset.filter(
        #             institution=institution_id, branch=branch_id, status=True).order_by('id')
        #     elif branch_id:
        #         queryset = queryset.filter(
        #             branch=branch_id, status=True).order_by('id')
        #     elif institution_id:
        #         queryset = queryset.filter(
        #             institution=institution_id, status=True).order_by('sl_no')
        #     else:
        #         queryset
        # except:
        #     pass
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

