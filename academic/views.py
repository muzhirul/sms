from django.shortcuts import render
from rest_framework import generics, permissions
from sms.utils import CustomResponse
from .models import *
from .serializers import *
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView

# Create your views here.
class VersionList(generics.ListCreateAPIView):
    queryset = Version.objects.all()
    serializer_class = VersionSerializer
    permission_classes = [permissions.IsAuthenticated]  # Requires a valid JWT token for access
    
    def list(self,request,*args, **kwargs):
        # serializer_class = TokenObtainPairView  # Create this serializer
        version = self.get_queryset()
        serializer = self.get_serializer(version,many=True)
        return CustomResponse(code=status.HTTP_200_OK, message="Success", data=serializer.data)
        