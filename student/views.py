from django.shortcuts import render
from rest_framework import generics, permissions
from sms.utils import CustomResponse
from .models import *
# from .serializers import *
from rest_framework import status

# Create your views here.
class StudentList(generics.ListCreateAPIView):
    pass