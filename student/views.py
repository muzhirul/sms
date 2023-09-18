from django.shortcuts import render
from rest_framework import generics, permissions
from sms.utils import CustomResponse
from .models import *
from .serializers import *
from sms.pagination import CustomPagination
from rest_framework import status
from authentication.models import Authentication
from rest_framework.response import Response

# Create your views here.
class StudentList(generics.ListCreateAPIView):
    serializer_class = StudentSerializer
    permission_classes = [permissions.IsAuthenticated]  # Requires a valid JWT token for access
    pagination_class = CustomPagination
    
    def get_queryset(self):
        queryset = Student.objects.filter(status=True).order_by('id')
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
    
    def create(self,request,*args, **kwargs):
        data = request.data
        student_data = data.copy()
        guardians_data = student_data.pop('guardians', [])
        # Create the student
        student_serializer = self.get_serializer(data=student_data)
        try:
            if student_serializer.is_valid():
                student_serializer.is_valid(raise_exception=True)
                institution_data = student_serializer.validated_data.get('institution')
                branch_data = student_serializer.validated_data.get('branch')
                # If data is provided, use it; otherwise, use the values from the request user
                institution = institution_data if institution_data is not None else self.request.user.institution
                branch = branch_data if branch_data is not None else self.request.user.branch
                student = student_serializer.save(Institution=institution, branch=branch)
                # Create the guardian and associate with the student
                guardians = []
                for guardian_data in guardians_data:
                    guardian_data['student'] = student.id
                    guardian_serializer = GuardianSerializer(data=guardian_data)
                    guardian_serializer.is_valid(raise_exception=True)
                    guardian = guardian_serializer.save()
                    guardians.append(guardian)
                response_data = student_serializer.data
                response_data['guardians'] = GuardianSerializer(guardians, many=True).data
        except Exception as e:
            # Handle other exceptions
            return CustomResponse(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="An error occurred during the Create", data=str(e))
            
        return Response(response_data, status=status.HTTP_201_CREATED)