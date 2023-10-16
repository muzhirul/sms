from rest_framework import serializers
from academic.models import *
from setup_app.serializers import FloorTypeSerializer, DaySerializer
from staff.serializers import StaffTeacherSerializer

class VersionSerializer2(serializers.ModelSerializer):
    class Meta:
        model = Version
        fields = ['id','version']

class VersionSerializer(serializers.ModelSerializer):
    created_username = serializers.ReadOnlyField(source='created_by.username')
    updated_username = serializers.ReadOnlyField(source='created_by.username')
    institution_name = serializers.ReadOnlyField(source='institution.name')
    branch_name = serializers.ReadOnlyField(source='branch.name')
    class Meta:
        model = Version
        # Exclude the 'status' field and other fields you want to exclude
        exclude = ['status','code','start_date','end_date']
        # exclude = ['created_by', 'updated_by', 'created_at', 'updated_at']
        
class SessionSerializer2(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = ['id','session']

class SessionSerializer(serializers.ModelSerializer):
    created_username = serializers.ReadOnlyField(source='created_by.username')
    updated_username = serializers.ReadOnlyField(source='created_by.username')
    institution_name = serializers.ReadOnlyField(source='institution.name')
    branch_name = serializers.ReadOnlyField(source='branch.name')
    class Meta:
        model = Session
        # Exclude the specified fields from serialization
        exclude = ['status','code']
        read_only_fields = ('code',)

class SectionSerializer2(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = ['id','section']

class SectionSerializer(serializers.ModelSerializer):
    created_username = serializers.ReadOnlyField(source='created_by.username')
    updated_username = serializers.ReadOnlyField(source='created_by.username')
    institution_name = serializers.ReadOnlyField(source='institution.name')
    branch_name = serializers.ReadOnlyField(source='branch.name')
    class Meta:
        model = Section
        # Exclude the specified fields from serialization
        exclude = ['status','code']
        read_only_fields = ('code',)


class SubjectSerializer(serializers.ModelSerializer):
    created_username = serializers.ReadOnlyField(source='created_by.username')
    updated_username = serializers.ReadOnlyField(source='created_by.username')
    institution_name = serializers.ReadOnlyField(source='institution.name')
    branch_name = serializers.ReadOnlyField(source='branch.name')
    class Meta:
        model = Subject
        # Exclude the specified fields from serialization
        exclude = ['status','start_date','end_date']
        
class SubjectSerializer2(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id','type','name','picture']

class ClassSerializer2(serializers.ModelSerializer):
    class Meta:
        model = ClassName
        fields = ['id','name']

class ClassSerializer(serializers.ModelSerializer):
    created_username = serializers.ReadOnlyField(source='created_by.username')
    updated_username = serializers.ReadOnlyField(source='created_by.username')
    institution_name = serializers.ReadOnlyField(source='institution.name')
    branch_name = serializers.ReadOnlyField(source='branch.name')
    class Meta:
        model = ClassName
        # Exclude the specified fields from serialization
        exclude = ['status','code']

class ClassRoomSerializer2(serializers.ModelSerializer):
    class Meta:
        model = ClassRoom
        fields =['id','room_no']

class ClassRoomSerializer(serializers.ModelSerializer):
    created_username = serializers.ReadOnlyField(source='created_by.username')
    updated_username = serializers.ReadOnlyField(source='created_by.username')
    institution_name = serializers.ReadOnlyField(source='institution.name')
    branch_name = serializers.ReadOnlyField(source='branch.name')
    floor_type= FloorTypeSerializer(read_only=True)
    class Meta:
        model = ClassRoom
        # Exclude the specified fields from serialization
        exclude = ('status',)
        # fields = ('building', 'room_no', 'floor_type','floor')
        
class ClassRoomSerializer3(serializers.ModelSerializer):
    class Meta:
        model = ClassRoom
        # Exclude the specified fields from serialization
        exclude = ('status',)
        
class ClassPeriodSerializer2(serializers.ModelSerializer):
    class Meta:
        model = ClassPeriod
        fields = ['id','name','start_time','end_time','duration']

class ClassPeriodSerializer(serializers.ModelSerializer):
    created_username = serializers.ReadOnlyField(source='created_by.username')
    updated_username = serializers.ReadOnlyField(source='created_by.username')
    institution_name = serializers.ReadOnlyField(source='institution.name')
    branch_name = serializers.ReadOnlyField(source='branch.name')
    class Meta:
        model = ClassPeriod
        # Exclude the specified fields from serialization
        exclude = ['status','code']


class ClassSectionSerializer(serializers.ModelSerializer):
    created_username = serializers.ReadOnlyField(source='created_by.username')
    updated_username = serializers.ReadOnlyField(source='created_by.username')
    institution_name = serializers.ReadOnlyField(source='institution.name')
    branch_name = serializers.ReadOnlyField(source='branch.name')
    class_name = ClassSerializer2(read_only=True)
    session = SessionSerializer2(read_only=True)
    section = SectionSerializer2(read_only=True)
    class Meta:
        model = ClassSection
        # Exclude the specified fields from serialization
        exclude = ['status']
        
class ClassSectionSerializer3(serializers.ModelSerializer):
    class Meta:
        model = ClassSection
        # Exclude the specified fields from serialization
        exclude = ['status']

        
class ClassSubjectSerializer(serializers.ModelSerializer):
    created_username = serializers.ReadOnlyField(source='created_by.username')
    updated_username = serializers.ReadOnlyField(source='created_by.username')
    institution_name = serializers.ReadOnlyField(source='institution.name')
    branch_name = serializers.ReadOnlyField(source='branch.name')
    class_name = ClassSerializer2(read_only=True)
    section = SectionSerializer2(read_only=True)
    session = SessionSerializer2(read_only=True)
    version = VersionSerializer2(read_only=True)
    class Meta:
        model = ClassSubject
        # Exclude the specified fields from serialization
        exclude = ['status']

class ClassSubjectSerializer2(serializers.ModelSerializer):
    
    class Meta:
        model = ClassSubject
        # Exclude the specified fields from serialization
        exclude = ['status']

        
class ClassRoutineSerializer(serializers.ModelSerializer):
    teacher = StaffTeacherSerializer(read_only=True)
    class_name = ClassSerializer2(read_only=True)
    section = SectionSerializer2(read_only=True)
    session = SessionSerializer2(read_only=True)
    version = VersionSerializer2(read_only=True)
    subject = SubjectSerializer2(read_only=True)
    class_period = ClassPeriodSerializer2(read_only=True)
    day = DaySerializer(read_only=True)
    class_room = ClassRoomSerializer2(read_only=True)
    class Meta:
        model = ClassRoutine
        fields = ['id','teacher','class_name','section','session','version','subject','class_period','day','class_room']
        
class ClassRoutineSerializer2(serializers.ModelSerializer):
    
    class Meta:
        model = ClassRoutine
        fields = ['id','teacher','class_name','section','session','version','subject','class_period','day','class_room']