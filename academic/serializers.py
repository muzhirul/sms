from rest_framework import serializers
from academic.models import *
from setup_app.serializers import FloorTypeSerializer, DaySerializer, SubjectTypeSerializer
from staff.serializers import StaffTeacherSerializer,StaffTeacherViewSerializer

class VersionSerializer2(serializers.ModelSerializer):
    class Meta:
        model = Version
        fields = ['id','version']

    def to_representation(self, instance):
        # Only include instances where status is True
        if instance.status:
            return super().to_representation(instance)
        else:
            # If status is False, return an empty dictionary
            return {}

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

    def to_representation(self, instance):
        # Only include instances where status is True
        if instance.status:
            return super().to_representation(instance)
        else:
            # If status is False, return an empty dictionary
            return {}

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

    def to_representation(self, instance):
        # Only include instances where status is True
        if instance.status:
            return super().to_representation(instance)
        else:
            # If status is False, return an empty dictionary
            return {}

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

class SubjectSerializer3(serializers.ModelSerializer):
    class Meta:
        model = Subject
        # Exclude the specified fields from serialization
        exclude = ['status','start_date','end_date']

    def to_representation(self, instance):
        # Only include instances where status is True
        if instance.status:
            return super().to_representation(instance)
        else:
            # If status is False, return an empty dictionary
            return {}

class SubjectViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id','name']
    
    def to_representation(self, instance):
        # Only include instances where status is True
        if instance.status:
            return super().to_representation(instance)
        else:
            # If status is False, return an empty dictionary
            return {}

class SubjectSerializer(serializers.ModelSerializer):
    created_username = serializers.ReadOnlyField(source='created_by.username')
    updated_username = serializers.ReadOnlyField(source='created_by.username')
    institution_name = serializers.ReadOnlyField(source='institution.name')
    branch_name = serializers.ReadOnlyField(source='branch.name')
    type = SubjectTypeSerializer(read_only=True)
    class Meta:
        model = Subject
        # Exclude the specified fields from serialization
        exclude = ['status','start_date','end_date']
        
class SubjectSerializer2(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id','type','name','picture']

    def to_representation(self, instance):
        # Only include instances where status is True
        if instance.status:
            return super().to_representation(instance)
        else:
            # If status is False, return an empty dictionary
            return {}

class ClassSerializer2(serializers.ModelSerializer):
    class Meta:
        model = ClassName
        fields = ['id','name']

    def to_representation(self, instance):
        # Only include instances where status is True
        if instance.status:
            return super().to_representation(instance)
        else:
            # If status is False, return an empty dictionary
            return {}

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

    def to_representation(self, instance):
        # Only include instances where status is True
        if instance.status:
            return super().to_representation(instance)
        else:
            # If status is False, return an empty dictionary
            return {}

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

    def to_representation(self, instance):
        # Only include instances where status is True
        if instance.status:
            return super().to_representation(instance)
        else:
            # If status is False, return an empty dictionary
            return {}
        
class ClassPeriodSerializer2(serializers.ModelSerializer):
    class Meta:
        model = ClassPeriod
        fields = ['id','name','start_time','end_time','duration']

    def to_representation(self, instance):
        # Only include instances where status is True
        if instance.status:
            return super().to_representation(instance)
        else:
            # If status is False, return an empty dictionary
            return {}

class ClassPeriodSerializer(serializers.ModelSerializer):
    created_username = serializers.ReadOnlyField(source='created_by.username')
    updated_username = serializers.ReadOnlyField(source='created_by.username')
    institution_name = serializers.ReadOnlyField(source='institution.name')
    branch_name = serializers.ReadOnlyField(source='branch.name')
    class Meta:
        model = ClassPeriod
        # Exclude the specified fields from serialization
        exclude = ['status','code']

class ClassGroupViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = ClassGroup
        exclude = ['status']

    def to_representation(self, instance):

        if instance.status:
            return super().to_representation(instance)
        else:
            return None

class ClassGroupCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = ClassGroup
        exclude = ['status']

class ClassSectionSerializer(serializers.ModelSerializer):
    created_username = serializers.ReadOnlyField(source='created_by.username')
    updated_username = serializers.ReadOnlyField(source='created_by.username')
    institution_name = serializers.ReadOnlyField(source='institution.name')
    branch_name = serializers.ReadOnlyField(source='branch.name')
    version = VersionSerializer2(read_only=True)
    class_name = ClassSerializer2(read_only=True)
    session = SessionSerializer2(read_only=True)
    section = SectionSerializer2(read_only=True)
    group = ClassGroupViewSerializer(read_only=True)
    class Meta:
        model = ClassSection
        # Exclude the specified fields from serialization
        exclude = ['status']
        
class ClassSectionSerializer3(serializers.ModelSerializer):
    class Meta:
        model = ClassSection
        # Exclude the specified fields from serialization
        exclude = ['status']

    def to_representation(self, instance):
        # Only include instances where status is True
        if instance.status:
            return super().to_representation(instance)
        else:
            # If status is False, return an empty dictionary
            return {}
        
class ClassSubjectSerializer(serializers.ModelSerializer):
    created_username = serializers.ReadOnlyField(source='created_by.username')
    updated_username = serializers.ReadOnlyField(source='created_by.username')
    institution_name = serializers.ReadOnlyField(source='institution.name')
    branch_name = serializers.ReadOnlyField(source='branch.name')
    class_name = ClassSerializer2(read_only=True)
    section = SectionSerializer2(read_only=True)
    session = SessionSerializer2(read_only=True)
    version = VersionSerializer2(read_only=True)
    subject = SubjectViewSerializer(read_only=True)
    class Meta:
        model = ClassSubject
        # Exclude the specified fields from serialization
        exclude = ['status']

class ClassSubjectSerializer2(serializers.ModelSerializer):
        
    class Meta:
        model = ClassSubject
        # Exclude the specified fields from serialization
        exclude = ['status']

    def to_representation(self, instance):
        # Only include instances where status is True
        if instance.status:
            return super().to_representation(instance)
        else:
            # If status is False, return an empty dictionary
            return {}

class ClassTeacherViewSerializer(serializers.ModelSerializer):
    version = VersionSerializer2(read_only=True)
    session = SessionSerializer2(read_only=True)
    class_name = ClassSerializer2(read_only=True)
    section = SectionSerializer2(read_only=True)
    group = ClassGroupViewSerializer(read_only=True)
    teacher = StaffTeacherViewSerializer(read_only=True)
    created_username = serializers.ReadOnlyField(source='created_by.username')
    updated_username = serializers.ReadOnlyField(source='created_by.username')

    class Meta:
        model = ClassTeacher
        exclude = ['status']

class ClassTeacherCreateSerializer(serializers.ModelSerializer):
    # version = serializers.IntegerField(required=True)
    # session = serializers.IntegerField(required=True)
    # class_name = serializers.IntegerField(required=True)
    # section = serializers.IntegerField(required=True)
    # teacher = serializers.IntegerField(required=True)
    
    class Meta:
        model = ClassTeacher
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

    def to_representation(self, instance):
        # Only include instances where status is True
        if instance.status:
            return super().to_representation(instance)
        else:
            # If status is False, return an empty dictionary
            return {}

