from rest_framework import serializers
from setup_app.serializers import BloodGroupSerializer, GenderSerializer, ReligionSerializer,EducationBoardViewSerializer
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

class EducationViewSerializer(serializers.ModelSerializer):
    edu_board = EducationBoardViewSerializer(read_only=True)
    class Meta:
        model = Education
        exclude = ['status','created_at','updated_at','created_by','updated_by']

class EducationSerializer(serializers.ModelSerializer):
        
    class Meta:
        model = Education
        # fields = '__all__'
        exclude = ['status','created_at','updated_at','created_by','updated_by']
        
class StaffTeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = ['id','first_name','last_name','staff_id','user']

class staffSerializer(serializers.ModelSerializer):
    staff_education = EducationSerializer(many=True, required=False, read_only=True)

    class Meta:
        model = Staff
        # fields = ['first_nmae','last_name']
        exclude = ['code','user','institution','branch','status']

class StaffShiftListSerializer2(serializers.ModelSerializer):
    class Meta:
        model = StaffShift
        fields = ['id','name']
        
class staffSerializer2(serializers.ModelSerializer):
    staff_education = EducationViewSerializer(many=True, required=False, read_only=True)
    gender = GenderSerializer(read_only=True)
    religion = ReligionSerializer(read_only=True)
    blood_group = BloodGroupSerializer(read_only=True)
    designation = DesignationListSerializer(read_only=True)
    department = DepartmentListSerializer(read_only=True)
    shift = StaffShiftListSerializer2(read_only=True)
    # shift = StaffShiftListCreate(read_only=True)
    class Meta:
        model = Staff
        # fields = ['first_nmae','last_name']
        exclude = ['code','user','institution','branch','status']
        
class StaffShiftSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffShift
        exclude = ['status','code','start_date','end_date','start_buf_min','end_buf_min','institution','branch']