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