from rest_framework import serializers
from .models import *

class GuardianSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guardian
        # Exclude the 'status' field and other fields you want to exclude
        exclude = ['status','created_by', 'updated_by', 'created_at', 'updated_at']

class StudentSerializer(serializers.ModelSerializer):
    student_guardian = GuardianSerializer(many=True, required=False)
    class Meta:
        model = Student
        # Exclude the 'status' field and other fields you want to exclude
        exclude = ['status','created_by', 'updated_by', 'created_at', 'updated_at']
        
