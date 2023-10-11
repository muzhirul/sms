from rest_framework import serializers
from staff.models import *

class DepartmentSerializer(serializers.ModelSerializer):
    created_username = serializers.ReadOnlyField(source='created_by.username')
    updated_username = serializers.ReadOnlyField(source='created_by.username')
    institution_name = serializers.ReadOnlyField(source='institution.name')
    branch_name = serializers.ReadOnlyField(source='branch.name')
    class Meta:
        model = Department
        # Exclude the 'status' field and other fields you want to exclude
        exclude = ['status','code']
        # exclude = ['created_by', 'updated_by', 'created_at', 'updated_at']

class DepartmentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id','name']
        
class DesignationSerializer(serializers.ModelSerializer):
    created_username = serializers.ReadOnlyField(source='created_by.username')
    updated_username = serializers.ReadOnlyField(source='created_by.username')
    institution_name = serializers.ReadOnlyField(source='institution.name')
    branch_name = serializers.ReadOnlyField(source='branch.name')
    class Meta:
        model = Designation
        # Exclude the 'status' field and other fields you want to exclude
        exclude = ['status','code']
        # exclude = ['created_by', 'updated_by', 'created_at', 'updated_at']

class DesignationListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Designation
        fields = ['id','name']
        
class EducationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Education
        fields = '__all__'
    
class staffSerializer(serializers.ModelSerializer):
    staff_education = EducationSerializer(many=True, required=False, read_only=True)

    class Meta:
        model = Staff
        # fields = ['first_nmae','last_name']
        fields = '__all__'