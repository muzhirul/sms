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