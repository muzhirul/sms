from rest_framework import serializers
from academic.models import *

class VersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Version
        # Exclude the 'status' field and other fields you want to exclude
        exclude = ['created_by', 'updated_by', 'created_at', 'updated_at']


class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        # Exclude the specified fields from serialization
        exclude = ['status', 'created_by', 'updated_by', 'created_at', 'updated_at']
        read_only_fields = ('code',)



class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        # Exclude the specified fields from serialization
        exclude = ['status', 'created_by', 'updated_by', 'created_at', 'updated_at']
        read_only_fields = ('code',)


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        # Exclude the specified fields from serialization
        exclude = ['status', 'created_by', 'updated_by', 'created_at', 'updated_at']


class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassName
        # Exclude the specified fields from serialization
        exclude = ['status', 'created_by', 'updated_by', 'created_at', 'updated_at']


class ClassRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassRoom
        # Exclude the specified fields from serialization
        exclude = ['status', 'created_by', 'updated_by', 'created_at', 'updated_at']


class ClassPeriodSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassPeriod
        # Exclude the specified fields from serialization
        exclude = ['status', 'created_by', 'updated_by', 'created_at', 'updated_at']


class ClassSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassSection
        # Exclude the specified fields from serialization
        exclude = ['status', 'created_by', 'updated_by', 'created_at', 'updated_at']
        
class ClassSubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassSubject
        # Exclude the specified fields from serialization
        exclude = ['status', 'created_by', 'updated_by', 'created_at', 'updated_at']