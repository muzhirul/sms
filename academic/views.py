from django.shortcuts import render
from rest_framework import generics, permissions
from sms.utils import CustomResponse
from .models import *
from .serializers import *
from rest_framework import status
# from rest_framework_simplejwt.views import TokenObtainPairView
from sms.pagination import CustomPagination
from rest_framework.response import Response

# Create your views here.
class VersionList(generics.ListCreateAPIView):
    queryset = Version.objects.all().order_by('id')
    serializer_class = VersionSerializer
    permission_classes = [permissions.IsAuthenticated]  # Requires a valid JWT token for access
    pagination_class = CustomPagination
    
    
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
        
        if serializer.is_valid():
            instance = serializer.save()
            # Customize the response data
            response_data = {
                "code": status.HTTP_201_CREATED,  # Status code for successful creation
                "message": "Version created successfully",
                "data": VersionSerializer(instance).data,
            }
                
            return Response(response_data, status=status.HTTP_201_CREATED)
        
        # If the serializer is not valid, return an error response
        error_data = {
            "code": status.HTTP_400_BAD_REQUEST,  # Status code for validation error
            "message": "Validation error",
            "errors": serializer.errors,
        }
        
        return Response(error_data, status=status.HTTP_400_BAD_REQUEST)





        