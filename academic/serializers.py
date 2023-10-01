from rest_framework import serializers
from academic.models import *

class VersionSerializer(serializers.ModelSerializer):
    created_username = serializers.ReadOnlyField(source='created_by.username')
    updated_username = serializers.ReadOnlyField(source='created_by.username')
    class Meta:
        model = Version
        # Exclude the 'status' field and other fields you want to exclude
        exclude = ['created_by', 'updated_by', 'created_at', 'updated_at']


class SessionSerializer(serializers.ModelSerializer):
    created_username = serializers.ReadOnlyField(source='created_by.username')
    updated_username = serializers.ReadOnlyField(source='created_by.username')
    class Meta:
        model = Session
        # Exclude the specified fields from serialization
        exclude = ['status']
        read_only_fields = ('code',)



class SectionSerializer(serializers.ModelSerializer):
    created_username = serializers.ReadOnlyField(source='created_by.username')
    updated_username = serializers.ReadOnlyField(source='created_by.username')
    class Meta:
        model = Section
        # Exclude the specified fields from serialization
        exclude = ['status']
        read_only_fields = ('code',)


class SubjectSerializer(serializers.ModelSerializer):
    created_username = serializers.ReadOnlyField(source='created_by.username')
    updated_username = serializers.ReadOnlyField(source='created_by.username')
    class Meta:
        model = Subject
        # Exclude the specified fields from serialization
        exclude = ['status']


class ClassSerializer(serializers.ModelSerializer):
    created_username = serializers.ReadOnlyField(source='created_by.username')
    updated_username = serializers.ReadOnlyField(source='created_by.username')
    class Meta:
        model = ClassName
        # Exclude the specified fields from serialization
        exclude = ['status']


class ClassRoomSerializer(serializers.ModelSerializer):
    created_username = serializers.ReadOnlyField(source='created_by.username')
    updated_username = serializers.ReadOnlyField(source='created_by.username')
    class Meta:
        model = ClassRoom
        # Exclude the specified fields from serialization
        exclude = ['status']


class ClassPeriodSerializer(serializers.ModelSerializer):
    created_username = serializers.ReadOnlyField(source='created_by.username')
    updated_username = serializers.ReadOnlyField(source='created_by.username')
    class Meta:
        model = ClassPeriod
        # Exclude the specified fields from serialization
        exclude = ['status']


class ClassSectionSerializer(serializers.ModelSerializer):
    created_username = serializers.ReadOnlyField(source='created_by.username')
    updated_username = serializers.ReadOnlyField(source='created_by.username')
    class Meta:
        model = ClassSection
        # Exclude the specified fields from serialization
        exclude = ['status']
        
class ClassSubjectSerializer(serializers.ModelSerializer):
    created_username = serializers.ReadOnlyField(source='created_by.username')
    updated_username = serializers.ReadOnlyField(source='created_by.username')
    class Meta:
        model = ClassSubject
        # Exclude the specified fields from serialization
        exclude = ['status']