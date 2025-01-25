
from rest_framework import serializers
from .models import Authentication
from student.models import Student, Guardian
from staff.models import Staff
from django.contrib.auth.models import Group, Permission
from django.contrib import auth
from django.contrib.contenttypes.models import ContentType
from institution.serializers import *


class ContentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentType
        fields = ['id','app_label','model']
        ordering = ('id',)
        
class PermissionSerializer(serializers.ModelSerializer):
    menu = ContentTypeSerializer(read_only=True, source='content_type')  # Include group permissions
    class Meta:
        model = Permission
        fields = ['id', 'name', 'codename','menu']

class GroupSerializer(serializers.ModelSerializer):
    permissions = PermissionSerializer(many=True, read_only=True)  # Include group permissions
    class Meta:
        model = Group
        fields = ['name', 'permissions']

class LoginSerializer(serializers.ModelSerializer):
    # groups = GroupSerializer(many=True, read_only=True)  # Include user groups
    roles = GroupSerializer(many=True, read_only=True, source='groups')  # Change groups_data to roles
    username = serializers.CharField(max_length=50,min_length=3)
    password = serializers.CharField(max_length=68, min_length=5, write_only=True)
    
    
    class Meta:
        model = Authentication
        fields = ['id','username','first_name','last_name','user_type','password','roles']
        
class LoginSerializer2(serializers.ModelSerializer):
    username = serializers.CharField(max_length=50,min_length=3)
    password = serializers.CharField(max_length=68, min_length=5, write_only=True)
    
    
    class Meta:
        model = Authentication
        fields = ['id','username','first_name','last_name','user_type','institution','branch','password']
        
class LoginSerializer3(serializers.ModelSerializer):
    username = serializers.CharField(max_length=50,min_length=3)
    password = serializers.CharField(max_length=68, min_length=5, write_only=True)
    class Meta:
        model = Authentication
        fields = ['id','username','first_name','last_name','user_type','institution','branch','password']
    
class LoginSerializer4(serializers.ModelSerializer):
    username = serializers.CharField(max_length=50,min_length=3)
    password = serializers.CharField(max_length=68, min_length=5, write_only=True)
    institution = InstitutionViewSerializer(read_only=True)
    branch = BranchViewSerializer(read_only=True)
    class Meta:
        model = Authentication
        fields = ['id','username','institution','branch','password']

class UserViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = None
        fields = ['user','first_name','last_name']

    def __init__(self, *args, **kwargs):
        super(UserViewSerializer, self).__init__(*args, **kwargs)
        # Dynamically set the model and fields based on user_type
        user_type = self.context['request'].query_params.get('user_type')
        if user_type == 'student':
            self.Meta.model = Student
            self.Meta.fields = ['user','id','student_no','first_name','last_name']
        elif user_type == 'guardian':
            self.Meta.model = Guardian
            self.Meta.fields = ['user','id','guardian_no','first_name','last_name']
        else:
            self.Meta.model = Staff
            self.Meta.fields = ['user','id','staff_id','first_name','last_name']