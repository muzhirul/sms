from rest_framework import serializers
from .models import Authentication
from django.contrib.auth.models import Group, Permission

class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ('id', 'name', 'codename')

class GroupSerializer(serializers.ModelSerializer):
    permissions = PermissionSerializer(many=True, read_only=True)  # Include group permissions
    
    class Meta:
        model = Group
        fields = ('name', 'permissions')

class LoginSerializer(serializers.ModelSerializer):
    # groups = GroupSerializer(many=True, read_only=True)  # Include user groups
    roles = GroupSerializer(many=True, read_only=True, source='groups')  # Change groups_data to roles_data
    username = serializers.CharField(max_length=50,min_length=3)
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    
    class Meta:
        model = Authentication
        fields = ['id','username','first_name','last_name','user_type','password','roles']