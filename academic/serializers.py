from rest_framework import serializers
from academic.models import *
from setup_app.serializers import FloorTypeSerializer

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


class ClassSerializer(serializers.ModelSerializer):
    created_username = serializers.ReadOnlyField(source='created_by.username')
    updated_username = serializers.ReadOnlyField(source='created_by.username')
    institution_name = serializers.ReadOnlyField(source='institution.name')
    branch_name = serializers.ReadOnlyField(source='branch.name')
    class Meta:
        model = ClassName
        # Exclude the specified fields from serialization
        exclude = ['status','code']


class ClassRoomSerializer(serializers.ModelSerializer):
    created_username = serializers.ReadOnlyField(source='created_by.username')
    updated_username = serializers.ReadOnlyField(source='created_by.username')
    institution_name = serializers.ReadOnlyField(source='institution.name')
    branch_name = serializers.ReadOnlyField(source='branch.name')
    floor_type = FloorTypeSerializer(read_only=True)
    class Meta:
        model = ClassRoom
        # Exclude the specified fields from serialization
        exclude = ('status',)
        # fields = ('building', 'room_no', 'floor_type','floor')


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
    class Meta:
        model = ClassSection
        # Exclude the specified fields from serialization
        exclude = ['status','code']
        
class ClassSubjectSerializer(serializers.ModelSerializer):
    created_username = serializers.ReadOnlyField(source='created_by.username')
    updated_username = serializers.ReadOnlyField(source='created_by.username')
    institution_name = serializers.ReadOnlyField(source='institution.name')
    branch_name = serializers.ReadOnlyField(source='branch.name')
    class Meta:
        model = ClassSubject
        # Exclude the specified fields from serialization
        exclude = ['status','code']
        
class ClassRoutineSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ClassRoutine
        fields = ['id','teacher','class_name','section','session','version','subject','class_period','day','class_room']